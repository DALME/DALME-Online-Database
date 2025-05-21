import { Model } from "pinia-orm";

import { isObject } from "@/utils";

import { AttributeType } from "./attribute-type";

export class Metadata extends Model {
  static entity = "metadata";
  static primaryKey = "entity";

  static fields() {
    return {
      entity: this.string(""),
      attributeTypes: this.hasMany(AttributeType, "entity"),
      contentType: this.number(null),
    };
  }

  static saving(model) {
    if (
      "attributeTypes" in model &&
      Array.isArray(model.attributeTypes) &&
      isObject(model.attributeTypes[0])
    ) {
      model.attributeTypes.forEach((at) => {
        at.entity = model.entity;
      });
    }
  }

  static piniaExtend = {
    persist: true,
  };
}
