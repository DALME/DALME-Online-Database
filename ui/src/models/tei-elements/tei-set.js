import { Model } from "pinia-orm";
import TeiElement from "./tei-element";
import TeiSetMember from "./tei-set-member";

export default class TeiSet extends Model {
  static entity = "tei-set";

  static fields() {
    return {
      id: this.attr(null),
      label: this.string(""),
      description: this.string(""),
      project: this.string(""),
      isDefault: this.boolean(),
      elements: this.belongsToMany(TeiElement, TeiSetMember, "set", "element"),
    };
  }

  static piniaOptions = {
    persist: true,
  };
}
