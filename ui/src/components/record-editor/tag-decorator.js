import { h, render } from "vue";
import { Decoration, EditorView, ViewPlugin, WidgetType } from "@codemirror/view";
import { syntaxTree } from "@codemirror/language";
import { useSettingsStore } from "@/stores/settings";
import TeiTag from "./TeiTag.vue";
import { range, intersection, difference } from "ramda";

const tagPattern = /<(\/)?([a-z]+)([^>]+?)?(\/)?>/gi;
const tagAttributePattern = /([a-z0-9-:]+)=(".+?")/gi;

const deconstructTag = (text) => {
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

// const getPairedTag = (view, range, type) => {
//   console.log("called getPairedTag", range, type);
//   if (type.selfClose) return null;
//   try {
//     const dir = type.open ? 1 : -1;
//     const pos = type.open ? range.from : range.to;
//     const childType = type.open ? "CloseTag" : "OpenTag";
//     const match = matchBrackets(view.state, pos, dir);
//     const tree = ensureSyntaxTree(view.state, view.state.doc.length, 5000);
//     const node = tree.resolveInner(match.end.from).getChild(childType);
//     const { tag, attributes } = deconstructTag(view.state.doc.sliceString(node.from, node.to));
//     // console.log(match, node.name, view.state.doc.sliceString(node.from, node.to));
//     return { node, tag, attributes };
//   } catch (error) {
//     return error;
//   }
// };

class TagWidget extends WidgetType {
  constructor(data) {
    super();
    this.id = data.id;
    this.tag = data.tag;
    this.type = data.type;
    this.attributes = data.attributes || [];
    this.from = data.from;
    this.to = data.to;
    this.section = data.section;
    this.label = data.label;
    this.description = data.description || "";
    this.icon = data.icon;
    this.widgets = data.widgets;
    this.components = data.components;
    this.container = document.createElement("div");
    this.container.className = "cm-tag-widget-container";
    this.container.setAttribute("data-from", this.from);
    this.container.setAttribute("data-to", this.to);
    this.container.setAttribute("data-tag", this.tag);
    this.container.setAttribute("data-id", this.id);
    if (this.type == "CloseTag") {
      const tagDiv = document.createElement("div");
      tagDiv.className = `cm-tag-widget close ${this.section}`;
      const icon = document.createElement("i");
      icon.className = `q-icon ${this.icon} q-mx-auto`;
      tagDiv.appendChild(icon);
      this.container.appendChild(tagDiv);
    } else {
      this.widgets.value[this.id] = this;
    }
  }

  toDOM() {
    return this.container;
  }

  eq(other) {
    if (other.tag === this.tag && other.from === this.from && other.to === this.to) {
      return true;
    } else if (other.tag === this.tag) {
      // this = in place, other = newly generated
      console.log(`merging widgets this:${this.id} and other:${other.id}`);
      // console.log("this", this.id, this.from, this.to);
      // console.log("other", other.id, other.from, other.to);
      // this.id = other.id;
      this.from = other.from;
      this.to = other.to;
      this.container.setAttribute("data-from", this.from);
      this.container.setAttribute("data-to", this.to);
      return false;
    } else {
      return false;
    }
  }

  destroy() {
    console.log(`destroying widget ${this.id}`);
    // delete this.widgets.value[this.id];
    // this.container.dispatchEvent(
    //   new CustomEvent("widgetDestroyed", {
    //     bubbles: true,
    //     detail: { id: this.id },
    //   }),
    // );
    // return true;
  }

  updateDOM(elt, _view) {
    console.log("updateDOM called", this.from, this.to, this.id);
    elt.setAttribute("data-from", this.from);
    elt.setAttribute("data-to", this.to);
    return true;
  }
}

class TagDecorator {
  constructor(widgets, components) {
    this.settings = useSettingsStore();
    this.widgets = widgets;
    this.components = components;
    this.viewport_from = 0;
    this.viewport_to = 0;
  }

  createDeco(view) {
    this.viewport_from = view.viewport.from;
    this.viewport_to = view.viewport.to;
    const { ranges, changes } = this.getDecorations(view, this.viewport_from, this.viewport_to);
    return { decoration: Decoration.set(ranges, true), changes: changes };
  }

  updateDeco(update, decorations) {
    console.log("updateDeco called", update);
    let changeFrom = 1e9;
    let changeTo = update.view.viewport.to;
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
      try {
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
          const startLine = update.view.state.doc.line(targetRng.at(0)) || null;
          const endLine = update.view.state.doc.line(targetRng.at(-1)) || null;
          if (startLine) changeFrom = Math.min(startLine.from, changeFrom);
          if (endLine) changeTo = Math.max(endLine.to, changeTo);
        } else {
          // there is no overlap, so the entire viewport has changed
          changeFrom = update.view.viewport.from;
          changeTo = update.view.viewport.to;
        }
      } catch {
        changeFrom = update.view.viewport.from;
        changeTo = update.view.viewport.to;
      }
      console.log(`viewportMoved: changeFrom=${changeFrom}, changeTo=${changeTo}`);
    }

    if (changeTo - changeFrom > 10000) {
      console.log("changeTo - changeFrom > 1000");
      return this.createDeco(update.view);
    }

    if (changeTo > -1) {
      console.log("changeTo > -1");
      return this.updateRange(update.view, decorations, changeFrom, changeTo);
    }

    return { decoration: decorations, changes: [] };
  }

  updateRange(view, decorations, updateFrom, updateTo) {
    let changes = [];
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
        let result = this.getDecorations(view, start, end);
        decorations = decorations.update({
          filterFrom: start,
          filterTo: end,
          filter: (from, to) => from < start || to > end,
          add: result.ranges,
          sort: true,
        });
        changes = result.changes;
      }
    }
    return { decoration: decorations, changes: changes || [] };
  }

  getDecorations(view, from, to) {
    const ranges = [];
    const changes = [];
    // const tree = ensureSyntaxTree(view.state, view.state.doc.length, 5000);
    // https://discuss.codemirror.net/t/efficient-way-to-get-current-syntax-tree-to-extract-headers/3975/5
    syntaxTree(view.state).iterate({
      from,
      to,
      enter: (cursor) => {
        if (cursor.name === "Element") {
          // console.log("found element", cursor.node, cursor.from, cursor.to);
          if (cursor.node.firstChild.name !== "SelfClosingTag") {
            if (cursor.node.firstChild.name === "⚠" && cursor.node.lastChild.name === "CloseTag") {
              changes.push({ from: cursor.node.lastChild.from, to: cursor.node.lastChild.to });
              return true;
            } else if (
              cursor.node.firstChild.name === "OpenTag" &&
              cursor.node.lastChild.name === "⚠"
            ) {
              changes.push({ from: cursor.node.firstChild.from, to: cursor.node.firstChild.to });
              return true;
            }
          }
          const oTag = cursor.node.firstChild;
          const { tag, attributes, tagData, elData } = this.getTagData(view, oTag);
          if (this.settings.tags.names.includes(tag)) {
            const widgetId = crypto.randomUUID().replace(/-/g, "");
            const oWidget = new TagWidget({
              id: widgetId,
              tag: tag,
              type: oTag.name,
              attributes: this.generateAttributes(tagData.attributes, attributes, tagData.kind),
              from: oTag.from,
              to: oTag.to,
              section: elData.section,
              label: elData.label,
              description: elData.description,
              icon: tagData.icon || elData.icon,
              widgets: this.widgets,
              components: this.components,
            });
            if (oTag.name === "OpenTag") {
              const cTag = cursor.node.lastChild;
              console.log("found closing tag", cTag);
              const cWidget = new TagWidget({
                id: widgetId,
                tag: tag,
                type: cTag.name,
                from: cTag.from,
                to: cTag.to,
                section: elData.section,
                label: elData.label,
                icon: tagData.icon || elData.icon,
                widgets: this.widgets,
                components: this.components,
              });
              ranges.push(Decoration.replace({ widget: oWidget }).range(oTag.from, oTag.to));
              ranges.push(Decoration.replace({ widget: cWidget }).range(cTag.from, cTag.to));
            } else {
              ranges.push(Decoration.replace({ widget: oWidget }).range(oTag.from, oTag.to));
            }
          }
        }
      },
    });
    return { ranges, changes };
  }

  getTagData(view, node) {
    const { tag, attributes } = deconstructTag(view.state.doc.sliceString(node.from, node.to));
    const tagData = this.settings.tags.filter(tag, attributes);
    return {
      tag: tag,
      attributes: attributes,
      tagData: tagData.length ? tagData[0] : null,
      elData: tagData.length ? this.settings.elements.get(tagData[0].element) : null,
    };
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
}

export const tagDecoratorPlugin = (
  currentInstance,
  updateTag,
  widgetRegistry,
  componentRegistry,
) => {
  return ViewPlugin.fromClass(
    class {
      constructor(view) {
        console.log("creating tagPlugin");
        this.widgets = widgetRegistry;
        this.components = componentRegistry;
        this.updateTag = updateTag;
        this.tagMatcher = new TagDecorator(this.widgets, this.components);
        const { ranges, _changes } = this.tagMatcher.createDeco(view);
        this.tags = ranges;
        // if (changes.length) this.updateTag(changes);
        this.renderWidgets(this.tags);
      }

      destroy() {
        console.log("destroying tagPlugin");
      }

      update(update) {
        console.log("update called", update);
        if (
          update.docChanged ||
          update.viewportChanged ||
          syntaxTree(update.startState) != syntaxTree(update.state)
        ) {
          const { ranges, _changes } = this.tagMatcher.updateDeco(update, this.tags);
          this.tags = ranges;
          // if (changes.length) this.updateTag(changes);
          this.renderWidgets(this.tags);
        }
      }

      renderWidgets(decorations) {
        if (decorations) {
          for (let iter = decorations.iter(); iter.value !== null; iter.next()) {
            const widget = iter.value.widget;
            if (widget.type !== "CloseTag") {
              if (!widget.container.getAttribute("id")) {
                const compId = crypto.randomUUID().replace(/-/g, "");
                const component = h(TeiTag, {
                  id: compId,
                  widgetId: widget.id,
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
                component.ref = compId;
                component.appContext = currentInstance.appContext.app._context;
                widget.container.setAttribute("id", compId);
                widget.container.setAttribute("ref", compId);
                // console.log(`rendering ${compId}`);
                render(component, widget.container);
              } else {
                console.log(`component ${widget.container.getAttribute("id")} already rendered`);
              }
            }
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
