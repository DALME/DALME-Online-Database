import { Model } from "pinia-orm";
import TeiTag from "./tei-tag";

export default class TeiElement extends Model {
  static entity = "tei-element";

  static fields() {
    return {
      id: this.attr(null),
      label: this.string(""),
      section: this.string(""),
      description: this.string(""),
      kbReference: this.string(""),
      compound: this.boolean(),
      icon: this.string(""),
      tags: this.hasMany(TeiTag, "element"),
    };
  }

  static piniaOptions = {
    persist: true,
  };
}
