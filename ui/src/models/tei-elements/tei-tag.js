import { Model } from "pinia-orm";

import TeiElement from "./tei-element";

export default class TeiTag extends Model {
  static entity = "tei-tag";

  static fields() {
    return {
      id: this.attr(null),
      element: this.attr(null),
      name: this.string(""),
      kind: this.string(""),
      placeholder: this.string(""),
      parent: this.string(""),
      icon: this.string(""),
      attributes: this.attr([]),
      elementObj: this.belongsTo(TeiElement, "element"),
    };
  }

  static piniaOptions = {
    persist: true,
  };
}
