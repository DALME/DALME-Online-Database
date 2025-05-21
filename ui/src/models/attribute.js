import { useRepo } from "pinia-orm";

import { requests } from "@/api";
import { CustomModel, CustomRepository } from "@/models";
import { attributeListSchema, attributeSchema } from "@/schemas";

class Attribute extends CustomModel {
  static entity = "attribute";
  static requests = requests.attributes;
  static schema = {
    instance: attributeSchema,
    list: attributeListSchema,
  };

  static fields() {
    return {
      attributeType: this.number(null),
      dataType: this.string(""),
      description: this.string(""),
      id: this.attr(null),
      isUnique: this.boolean(false),
      label: this.string(""),
      name: this.string(""),
      objectId: this.attr(null),
      objectType: this.string(""),
      value: this.attr(null),
    };
  }
}

class AttributeRepo extends CustomRepository {
  use = Attribute;
}

export const Attributes = useRepo(AttributeRepo);
