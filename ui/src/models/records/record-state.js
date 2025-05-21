import { Model } from "pinia-orm";

import { PageState } from "./page-state";

export class RecordState extends Model {
  static entity = "record-state";

  static fields() {
    return {
      id: this.attr(null),
      currentPageId: this.attr(null),
      editOn: this.boolean(false),
      editorSplitter: this.number(null),
      lastSplitter: this.number(null),
      pageDrawerMini: this.boolean(false),
      showTagMenu: this.boolean(false),
      splitterHorizontal: this.boolean(false),
      tab: this.string("info"),
      pageStates: this.hasMany(PageState, "recordId"),
    };
  }

  static piniaExtend = {
    persist: true,
  };
}
