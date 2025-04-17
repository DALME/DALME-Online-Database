import { h, render } from "vue";
import { Decoration, EditorView, ViewPlugin, WidgetType } from "@codemirror/view";
import { matchBrackets, ensureSyntaxTree, syntaxTree } from "@codemirror/language";
import { useEditorStore } from "@/stores/editor";
import TeiTagMenu from "./TeiTagMenu.vue";

const tagPattern = /<(\/)?([a-z]+)([^>]+?)?(\/)?>/gi;
const tagAttributePattern = /([a-z0-9-:]+)=(".+?")/gi;

const deconstructTag = (text) => {
  if (text) {
    tagPattern.lastIndex = 0;
    let match = tagPattern.exec(text);
    match = match.filter(Boolean);
    const tag = match.at(1);
    const attributes = {};
    let m;
    while ((m = tagAttributePattern.exec(match.at(2)))) {
      attributes[m[1]] = m[2].replace(/"/g, "");
    }
    return { tag, attributes };
  }
  return null;
};

const getPairedTag = (state, node, type) => {
  // console.log("called getPairedTag", node, type);
  if (type.selfClose) return node;
  const dir = type.open ? 1 : -1;
  const pos = type.open ? node.from : node.to;
  const childType = type.open ? "CloseTag" : "OpenTag";
  const match = matchBrackets(state, pos, dir);
  if (match.matched) {
    const tree = ensureSyntaxTree(state, state.doc.length, 5000);
    const node = tree.resolve(type.close ? match.end.from : match.end.to).getChild(childType);
    return node;
  }
  return null;
};

const getTagDetail = (tag, attributes) => {
  if (tag === "table") {
    const rows = attributes.rows || null;
    const cols = attributes.cols || null;
    return rows && cols ? `${rows}x${cols}` : null;
  } else if (tag === "row" && attributes.role === "label") {
    return "H";
  } else if (tag === "num") {
    return attributes.value || null;
  } else if (tag === "g") {
    return attributes.ref ? String.fromCodePoint(`0x${attributes.ref}`) : null;
  } else {
    for (const attr of ["xml:id", "target", "columns", "n"]) {
      if (attr in attributes) {
        return attributes[attr];
      }
    }
  }
  return null;
};

class TagPill extends WidgetType {
  constructor({ tagData, type, attributes, from, to, instance, handler }) {
    super();
    this.tagData = tagData;
    this.type = type;
    this.attributes = attributes;
    this.from = from;
    this.to = to;
    this.icon = tagData.icon || tagData.elementObj.icon;
    this.detail = getTagDetail(tagData.name, attributes);
    this.container = this.getElement();
    this.menu = this.type.close ? null : this.getMenu(instance, handler);
  }

  getElement() {
    const container = document.createElement("div");
    container.className = "cm-tag-widget-container";

    const tagDiv = document.createElement("div");
    const typeClass = this.type.open ? "open" : this.type.selfClose ? "self-close" : "close";
    tagDiv.className = `cm-tag-widget ${typeClass} ${this.tagData.elementObj.section}`;

    const icon = document.createElement("i");
    icon.className = `q-icon ${this.icon} q-mx-auto`;
    icon.setAttribute("aria-hidden", true);
    icon.setAttribute("role", "presentation");

    if (this.type.close) {
      tagDiv.appendChild(icon);
      container.appendChild(tagDiv);
    } else {
      const marker = document.createElement("div");
      marker.className = "tag-marker";
      marker.appendChild(icon);
      if (this.detail) {
        const detailContainer = document.createElement("div");
        detailContainer.className = "tag-text";
        detailContainer.textContent = this.detail;
        marker.appendChild(detailContainer);
      }
      tagDiv.appendChild(marker);
      container.appendChild(tagDiv);
    }
    return container;
  }

  getMenu(instance, handler) {
    const component = h(TeiTagMenu, {
      tagData: this.tagData,
      elData: this.tagData.elementObj,
      attributes: this.attributes,
      from: this.from,
      to: this.to,
      onUpdate: handler,
    });
    component.appContext = instance.appContext.app._context;
    return component;
  }

  toDOM(_view) {
    if (!this.type.close) {
      render(this.menu, this.container);
    }
    return this.container;
  }

  eq(other) {
    if (other.tag === this.tag && other.from === this.from && other.to === this.to) {
      return true;
    } else if (other.tag === this.tag) {
      // this = in place, other = newly generated
      console.log(`merging widgets ${this.from}-${this.to} and ${other.from}-${other.to}`);
      this.from = other.from;
      this.to = other.to;
      return false;
    } else {
      return false;
    }
  }

  destroy() {
    console.log(`destroying widget ${this.from}-${this.to}`);
  }

  updateDOM(_elt, _view) {
    console.log("updateDOM called", this.from, this.to);
    // elt.setAttribute("data-from", this.from);
    // elt.setAttribute("data-to", this.to);
    return true;
  }
}

export const tagDecoratorPlugin = (currentInstance, updateTag) => {
  return ViewPlugin.fromClass(
    class {
      constructor(view) {
        console.log("creating tagPlugin");
        this.store = useEditorStore();
        this.compInstance = currentInstance;
        this.updateTag = updateTag;
        this.tags = this.getDecorations(view.state);
      }

      getDecorations(state) {
        const ranges = [];
        const changes = [];
        // const tree = ensureSyntaxTree(view.state, view.state.doc.length, 5000);
        // https://discuss.codemirror.net/t/efficient-way-to-get-current-syntax-tree-to-extract-headers/3975/5
        syntaxTree(state).iterate({
          enter: (node) => {
            if (node.name === "MismatchedCloseTag") {
              console.log("MISMATCHED TAG", node.name, node.from, node.to);
              changes.push({ from: node.from, to: node.to });
            } else if (["OpenTag", "CloseTag", "SelfClosingTag"].includes(node.name)) {
              const type = {
                open: node.name === "OpenTag",
                close: node.name === "CloseTag",
                selfClose: node.name === "SelfClosingTag",
              };
              const pairedTag = getPairedTag(state, node, type);
              // console.log("parser: node|paired", node.name, pairedTag);
              if (pairedTag !== null) {
                const { tag, attributes, tagData } = this.getTagData(
                  state,
                  type.close ? pairedTag : node,
                );
                // only continue if this is a TEI tag
                if (this.store.tagNames.includes(tag)) {
                  try {
                    const deco = Decoration.replace({
                      widget: new TagPill({
                        tagData: tagData,
                        type: type,
                        attributes: attributes,
                        from: node.from,
                        to: node.to,
                        instance: this.compInstance,
                        handler: this.updateTag,
                      }),
                    });
                    ranges.push(deco.range(node.from, node.to));
                  } catch (e) {
                    console.log("TagPill error", e, tag, attributes, tagData);
                  }
                }
              } else {
                console.log("ORPHAN TAG", node.name, node.from, node.to);
                changes.push({ from: node.from, to: node.to });
              }
            }
          },
        });
        if (changes.length) {
          this.updateTag(changes);
        }
        return Decoration.set(ranges);
      }

      getTagData(state, node) {
        // console.log("getTagData", node);
        const { tag, attributes } = deconstructTag(state.doc.sliceString(node.from, node.to));
        const tagData = this.store.tags(tag, attributes);
        return {
          tag: tag,
          attributes: attributes,
          tagData: tagData.length ? tagData[0] : null,
        };
      }

      update(update) {
        if (
          update.docChanged ||
          update.viewportChanged ||
          syntaxTree(update.startState) != syntaxTree(update.state)
        ) {
          console.log("update called", update);
          this.tags = this.getDecorations(update.state);
        }
      }

      destroy() {
        console.log("destroying tagPlugin");
      }
    },
    {
      decorations: (instance) => instance.tags,
      provide: (plugin) =>
        EditorView.atomicRanges.of((view) => {
          return view.plugin(plugin)?.tags || Decoration.none;
        }),
    },
  );
};
