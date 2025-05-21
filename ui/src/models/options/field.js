import { Model } from "pinia-orm";

import { isObject } from "@/utils";

import { Option } from "./option";

export class Field extends Model {
  static entity = "field";
  static primaryKey = ["field", "model"];

  static fields() {
    return {
      field: this.string(""),
      model: this.string(""),
      options: this.hasMany(Option, ["field", "model"]),
    };
  }

  static saving(model) {
    if ("options" in model && Array.isArray(model.options) && isObject(model.options[0])) {
      model.options?.forEach((option) => {
        console.log("saving option", model);
        option.field = model.field;
        option.model = model.model;
      });
    }
  }

  static piniaExtend = {
    persist: true,
  };
}
