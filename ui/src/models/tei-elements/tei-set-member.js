import { Model } from "pinia-orm";

import TeiElement from "./tei-element";

export default class TeiSetMember extends Model {
  static entity = "tei-set-member";
  static primaryKey = ["set", "element"];

  static fields() {
    return {
      set: this.attr(null),
      element: this.attr(null),
      inContextMenu: this.boolean(),
      inToolbar: this.boolean(),
      shortcut: this.string(""),
      elementObj: this.belongsTo(TeiElement, "element"),
    };
  }

  static piniaOptions = {
    persist: true,
  };
}
