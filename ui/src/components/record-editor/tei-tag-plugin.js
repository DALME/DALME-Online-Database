import { h, render } from "vue";
import { Decoration, EditorView, ViewPlugin, WidgetType } from "@codemirror/view";
import { syntaxTree, matchBrackets } from "@codemirror/language";
import { useSettingsStore } from "@/stores/settings";
import { difference, intersection, range } from "ramda";
import TeiTag from "./TeiTag.vue";

const tagPattern = /<(\/)?([a-z]+)([^>]+?)?(\/)?>/gi;
const tagAttributePattern = /([a-z0-9-:]+)=(".+?")/gi;

const deconstructTag = (text) => {
  // console.log("deconstructTag", text);
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
};

class TagWidget extends WidgetType {
  constructor({ tag, attributes, type, from, to, section, label, description, icon }) {
    super();
    this.tag = tag;
    this.attributes = attributes;
    this.type = type;
    this.from = from;
    this.to = to;
    this.section = section;
    this.label = label;
    this.description = description;
    this.icon = icon;
    const container = document.createElement("div");
    container.className = "cm-tag-widget-container";
    container.setAttribute("data-from", this.from);
    container.setAttribute("data-to", this.to);
    this.container = container;
  }

  toDOM() {
    return this.container;
  }

  eq(other) {
    if (other.tag === this.tag && other.from === this.from && other.to === this.to) {
      return true;
    } else if (other.tag === this.tag) {
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

  updateDOM(elt, _view) {
    console.log("updateDOM called", this.from, this.to);
    elt.setAttribute("data-from", this.from);
    elt.setAttribute("data-to", this.to);
    return true;
  }
}

class TagDecorator {
  constructor() {
    this.settings = useSettingsStore();
    this.viewport_from = 0;
    this.viewport_to = 0;
  }

  createDeco(view) {
    this.viewport_from = view.viewport.from;
    this.viewport_to = view.viewport.to;
    return Decoration.set(this.getDecorations(view, this.viewport_from, this.viewport_to));
  }

  updateDeco(update, decorations) {
    console.log("updateDeco called", update);
    let changeFrom = 1e9;
    let changeTo = -1;
    if (update.docChanged) {
      // the document has changed - map the changes to the decorations
      decorations = decorations.map(update.changes);
      // determine the range the combined changes
      update.changes.iterChanges((_f, _t, from, to) => {
        if (to >= update.view.viewport.from && from <= update.view.viewport.to) {
          changeFrom = Math.min(from, changeFrom);
          changeTo = Math.max(to, changeTo);
          console.log(`docChanged: changeFrom=${changeFrom}, changeTo=${changeTo}`);
        }
      });
    }

    if (!update.docChanged && update.viewportChanged) {
      // the document has not changed, but the viewport has
      // range of line numbers of the previous viewport
      const startRng = range(
        update.view.state.doc.lineAt(this.viewport_from).number,
        update.view.state.doc.lineAt(this.viewport_to).number + 1,
      );
      // range of line numbers of the updated viewport
      const endRng = range(
        update.view.state.doc.lineAt(update.view.viewport.from).number,
        update.view.state.doc.lineAt(update.view.viewport.to).number + 1,
      );
      // overlap of the two ranges
      const overlapRng = intersection(startRng, endRng);
      if (overlapRng.length) {
        // range of new lines visible after update -i.e. non-overlapping
        const targetRng = difference(endRng, overlapRng);
        changeFrom = Math.min(update.view.state.doc.line(targetRng.at(0)).from, changeFrom);
        changeTo = Math.max(update.view.state.doc.line(targetRng.at(-1)).to, changeTo);
      } else {
        // there is no overlap, so the entire viewport has changed
        changeFrom = update.view.viewport.from;
        changeTo = update.view.viewport.to;
      }
      console.log(`viewportMoved: changeFrom=${changeFrom}, changeTo=${changeTo}`);
    }

    if (changeTo - changeFrom > 1000) {
      console.log("changeTo - changeFrom > 1000");
      return this.createDeco(update.view);
    }

    if (changeTo > -1) {
      console.log("changeTo > -1");
      return this.updateRange(update.view, decorations, changeFrom, changeTo);
    }

    return decorations;
  }

  updateRange(view, decorations, updateFrom, updateTo) {
    for (let r of view.visibleRanges) {
      let from = Math.max(r.from, updateFrom);
      let to = Math.min(r.to, updateTo);
      console.log(`updateRange from=${from}, to=${to}`);
      if (to > from) {
        let fromLine = view.state.doc.lineAt(from);
        let toLine = fromLine.to < to ? view.state.doc.lineAt(to) : fromLine;
        let start = Math.max(r.from, fromLine.from);
        let end = Math.min(r.to, toLine.to);
        console.log(`updateRange start=${start}, end=${end}`);
        let ranges = this.getDecorations(view, start, end);
        decorations = decorations.update({
          filterFrom: start,
          filterTo: end,
          filter: (from, to) => from < start || to > end,
          add: ranges,
        });
      }
    }
    return decorations;
  }

  getDecorations(view, from, to) {
    const ranges = [];
    syntaxTree(view.state).iterate({
      from,
      to,
      enter: (node) => {
        if (["OpenTag", "CloseTag", "SelfClosingTag"].includes(node.name)) {
          const type = {
            open: node.name === "OpenTag",
            close: node.name === "CloseTag",
            selfClose: node.name === "SelfClosingTag",
          };
          const { tag, attributes, tagData, elData } = this.getTagData(view, node, type);
          // only continue if this is a TEI tag
          if (this.settings.tags.names.value.includes(tag)) {
            const deco = Decoration.replace({
              widget: new TagWidget({
                tag: tag,
                type: type,
                attributes: type.close
                  ? {}
                  : this.generateAttributes(tagData.attributes, attributes, tagData.kind),
                from: node.from,
                to: node.to,
                section: elData.section,
                label: elData.label,
                description: elData.description,
                icon: tagData.icon || elData.icon,
              }),
            });
            ranges.push(deco.range(node.from, node.to));
          }
        }
      },
    });
    return ranges;
  }

  getTagData(view, node, type) {
    let txtFrom, txtTo;
    if (type.close) {
      const matchTag = matchBrackets(view.state, node.to, -1);
      const matchNode = syntaxTree(view.state).resolve(matchTag.end.from);
      // console.log(matchTag, matchNode.name, matchNode.from, matchNode.to);
      txtFrom = matchNode.from;
      txtTo = matchNode.to;
    } else {
      txtFrom = node.from;
      txtTo = node.to;
    }
    const result = deconstructTag(view.state.doc.sliceString(txtFrom, txtTo));
    const tagData = this.settings.tags.filter(result.tag, result.attributes);
    if (tagData.length === 1) {
      result.tagData = tagData[0];
      result.elData = this.settings.elements.get(tagData[0].element);
    } else {
      console.log("tagData ERROR:", tagData, result.tag, result.attributes);
      result.tagData = null;
      result.elData = null;
    }
    return result;
  }

  generateAttributes(ref_attrs, attrs, kind) {
    let attributes = [];
    for (const attr of ref_attrs) {
      if (!(kind === "supplied" && attr.value === "text")) {
        let cValue;
        if (attr.value in attrs) {
          cValue = structuredClone(attrs[attr.value]);
        } else if (attr.default) {
          cValue = structuredClone(attr.default);
        } else {
          cValue = attr.kind === "multichoice" ? [] : "";
        }
        attributes.push({
          default: attr.label || null,
          description: attr.description,
          editable: attr.editable,
          required: attr.required,
          kind: attr.kind,
          label: attr.label,
          value: attr.value,
          options: attr.options || [],
          currentValue: cValue,
        });
      }
    }
    return attributes;
  }

  // findPairedTag(view, from, to) {
  //   for (let { from, to } of view.visibleRanges) {
  //     syntaxTree(view.state).iterate({
  //       from,
  //       to,
  //       enter: (node) => {
  //         if (node.name === "OpenTag") {
  //           const { tag, attributes, type } = deconstructTag(
  //             view.state.doc.sliceString(node.from, node.to),
  //           );
  //         }
  //       },
  //     });
  //   }
  // }
}

export const tagPlugin = (currentInstance, updateTag) => {
  return ViewPlugin.fromClass(
    class {
      constructor(view) {
        this.tagMatcher = new TagDecorator();
        this.tags = this.tagMatcher.createDeco(view);
        this.renderWidgets(this.tags);
      }

      destroy() {
        console.log("destroying tagPlugin");
      }

      update(update) {
        if (
          update.docChanged ||
          update.viewportChanged ||
          syntaxTree(update.startState) != syntaxTree(update.state)
        ) {
          this.tags = this.tagMatcher.updateDeco(update, this.tags);
          this.renderWidgets(this.tags);
        }
      }

      renderWidgets(decorations) {
        for (let iter = decorations.iter(); iter.value !== null; iter.next()) {
          const widget = iter.value.widget;
          if (!widget.container.getAttribute("id")) {
            const compId = crypto.randomUUID().replace(/-/g, "");
            const component = h(TeiTag, {
              id: compId,
              tag: widget.tag,
              attributes: widget.attributes,
              type: widget.type,
              from: widget.from,
              to: widget.to,
              section: widget.section,
              label: widget.label,
              description: widget.description,
              icon: widget.icon,
              domEl: widget.container,
              onUpdate: updateTag,
            });
            component.key = compId;
            component.appContext = currentInstance.appContext.app._context;
            widget.container.setAttribute("id", compId);
            console.log(`rendering ${compId}`);
            render(component, widget.container);
          } else {
            console.log(`component ${widget.container.getAttribute("id")} already rendered`);
          }
        }
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
