import { Model } from "pinia-orm";

export class Option extends Model {
  static entity = "option";

  static fields() {
    return {
      id: this.uid(),
      field: this.attr(null),
      model: this.attr(null),
      label: this.string(""),
      value: this.attr(null),
      group: this.string(""),
      detail: this.string(""),
      icon: this.string(""),
    };
  }

  static piniaExtend = {
    persist: true,
  };
}
