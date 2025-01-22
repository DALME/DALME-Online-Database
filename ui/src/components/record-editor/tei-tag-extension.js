import { RangeSetBuilder } from "@codemirror/state";
import { useSettingsStore } from "@/stores/settings";
import { mergeRight, sortBy, prop as rProp } from "ramda";
import { Decoration, WidgetType } from "@codemirror/view";

const tagPattern = /<(\/)?([a-z]+)([^>]+?)?(\/)?>/gi;
const tagAttributePattern = /([a-z0-9-:]+)=(".+?")/gi;

const deconstructTag = (match) => {
  match = match.filter(Boolean);
  const closing = match.at(1) === "/";
  const selfClosing = match.at(-1) === "/";
  const type = {
    open: !closing && !selfClosing,
    close: closing,
    selfClose: selfClosing,
  };
  const tag = closing ? match.at(2) : match.at(1);
  const attributes = {};
  if (!closing) {
    let m;
    while ((m = tagAttributePattern.exec(match.at(2)))) {
      attributes[m[1]] = m[2].replace(/"/g, "");
    }
  }
  return { tag, attributes, type };
};

const matchRanges = (view) => {
  let visible = view.visibleRanges;
  if (
    visible.length == 1 &&
    visible[0].from == view.viewport.from &&
    visible[0].to == view.viewport.to
  ) {
    return visible;
  }
  let result = [];
  for (let { from, to } of visible) {
    from = view.state.doc.lineAt(from).from;
    to = view.state.doc.lineAt(to).to;
    if (result.length && result[result.length - 1].to >= from) {
      result[result.length - 1].to = to;
    } else {
      result.push({ from, to });
    }
  }
  return result;
};

// export class widgetTracker {
//   constructor() {
//     this.store = {};
//   }

//   add(currentId, newId = null) {
//     this.store[currentId] = newId;
//     if (newId !== null) {
//       this.store[newId] = null;
//     }
//   }

//   get(id) {
//     while (id !== null) {
//       id = this.store[id];
//     }
//     return id;
//   }
// }

class TagWidget extends WidgetType {
  constructor({ id, tag, attributes, type, tagData, eData, from, to, pairing, tracker, queue }) {
    super();
    this.id = id;
    this.tag = tag;
    this.attributes = attributes;
    this.type = type;
    this.tagData = tagData;
    this.eData = eData;
    this.from = from;
    this.to = to;
    this.pairing = pairing;
    this.tracker = tracker;
    this.queue = queue;
    const container = document.createElement("div");
    container.className = "cm-tag-widget-container";
    container.setAttribute("data-widget", this.id);
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
      const trackerEntry = this.tracker.value.find((x) => x.widgets.includes(this.id));
      if (trackerEntry) {
        trackerEntry.widgets.push(other.id);
      }
      return false;
    } else {
      return false;
    }
  }

  destroy() {
    if (!this.type.selfClose) {
      const pairingIdx = this.tracker.value.findIndex((x) => x.widgets.includes(this.pairing));
      if (pairingIdx !== -1) {
        console.log(`pairingIdx=${pairingIdx}`);
        const pairingEl = document.getElementById(this.tracker.value[pairingIdx].component);
        console.log("pairingEl", pairingEl);
        if (pairingEl) {
          this.queue.value.push({
            from: pairingEl.getAttribute("data-from"),
            to: pairingEl.getAttribute("data-to"),
          });
          this.tracker.value.splice(pairingIdx, 1);
        }
      }
    }
    this.tracker.value.splice(
      this.tracker.value.findIndex((x) => x.widgets.includes(this.id)),
      1,
    );
    console.log(`destroying widget ${this.from}-${this.to}`);
  }

  updateDOM(elt, _view) {
    elt.setAttribute("data-widget", this.id);
    elt.setAttribute("data-from", this.from);
    elt.setAttribute("data-to", this.to);
    return true;
  }
}

export class TagDecorator {
  constructor(widgetTracker, changeQueue) {
    this.regexp = tagPattern;
    this.settings = useSettingsStore();
    this.viewport_to = 0;
    this.openTags = [];
    this.widgetTracker = widgetTracker;
    this.queue = changeQueue;
  }

  /// Compute the full set of decorations for matches in the given view's viewport.
  createDeco(view) {
    const build = new RangeSetBuilder();
    const add = build.add.bind(build);
    this.viewport_to = view.viewport.to;
    for (let { from, to } of matchRanges(view)) {
      this.iterMatches(view, from, to, add);
    }
    return build.finish();
  }

  iterMatches(view, from, to, callback) {
    this.regexp.lastIndex = 0;
    const tags = [];

    for (
      let cursor = view.state.doc.iterRange(from, to), pos = from, match;
      !cursor.next().done;
      pos += cursor.value.length
    ) {
      if (!cursor.lineBreak) {
        while ((match = this.regexp.exec(cursor.value))) {
          const { tag, attributes, type } = deconstructTag(match);
          if (!this.settings.tags.names.value.includes(tag)) {
            // not a TEI tag, so we skip it
            continue;
          }
          const id = crypto.randomUUID().replace(/-/g, "");
          if (!type.close) {
            const tagData = this.settings.tags.filter(tag, attributes);
            if (tagData.length !== 1) {
              console.log("tagData ERROR:", tagData, tag, attributes);
            }
            const eData = this.settings.elements.get(tagData[0].element);
            const newTag = {
              id: id,
              tag: tag,
              attributes: attributes,
              type: type,
              tagData: tagData[0],
              eData: eData,
              from: pos + match.index,
              to: pos + match.index + match[0].length,
            };
            if (eData.compound) {
              console.log("compound attributes", attributes);
            }
            if (type.open) {
              this.openTags.push(newTag);
            } else if (type.selfClose) {
              tags.push(newTag);
            }
          } else {
            const openTag = this.openTags.splice(
              this.openTags.findLastIndex((x) => x.tag === tag),
            )[0];
            if (openTag) {
              openTag.pairing = id;
              tags.push(openTag);
              tags.push(
                mergeRight(openTag, {
                  id: id,
                  tag: tag,
                  attributes: attributes,
                  type: type,
                  pairing: openTag.id,
                  from: pos + match.index,
                  to: pos + match.index + match[0].length,
                }),
              );
            }
          }
        }
      }
    }
    console.log("itertags", tags);
    sortBy(rProp("from"), tags).forEach((x) => {
      this.widgetTracker.value.push({ widgets: [x.id], data: x });
      x["tracker"] = this.widgetTracker;
      x["queue"] = this.queue;
      callback(x.from, x.to, Decoration.replace({ widget: new TagWidget(x) }));
    });
  }

  /// Update a set of decorations for a view update. `deco` _must_ be
  /// the set of decorations produced by _this_ `MatchDecorator` for
  /// the view state before the update.
  updateDeco(update, deco) {
    console.log("updateDeco called", update);
    let changeFrom = 1e9;
    let changeTo = -1;
    if (update.docChanged) {
      console.log("update.docChanged");
      update.changes.iterChanges((_f, _t, from, to) => {
        if (to >= update.view.viewport.from && from <= update.view.viewport.to) {
          changeFrom = Math.min(from, changeFrom);
          changeTo = Math.max(to, changeTo);
          console.log(`changeFrom=${changeFrom}, changeTo=${changeTo}`);
        }
      });
    }

    if (!update.docChanged && update.viewportChanged) {
      console.log(`update.viewportMoved: ${update.view.viewport.from}-${update.view.viewport.to}`);
      if (update.view.viewport.to > this.viewport_to) {
        changeFrom = this.viewport_to;
        changeTo = update.view.viewport.to;
      }
    }

    if (changeTo > -1) {
      console.log("changeTo > -1");
      return this.updateRange(update.view, deco.map(update.changes), changeFrom, changeTo);
    }

    return deco;
  }

  updateRange(view, deco, updateFrom, updateTo) {
    for (let r of view.visibleRanges) {
      let from = Math.max(r.from, updateFrom);
      let to = Math.min(r.to, updateTo);
      if (to > from) {
        let fromLine = view.state.doc.lineAt(from);
        let toLine = fromLine.to < to ? view.state.doc.lineAt(to) : fromLine;
        let start = Math.max(r.from, fromLine.from);
        let end = Math.min(r.to, toLine.to);
        let ranges = [];
        let add = (from, to, deco) => ranges.push(deco.range(from, to));
        this.iterMatches(view, start, end, add);
        deco = deco.update({
          filterFrom: start,
          filterTo: end,
          filter: (from, to) => from < start || to > end,
          add: ranges,
        });
      }
    }
    return deco;
  }
}
