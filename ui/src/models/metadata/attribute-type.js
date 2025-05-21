import { Model } from "pinia-orm";

export class AttributeType extends Model {
  static entity = "attribute-type";

  static fields() {
    return {
      dataType: this.string(""),
      description: this.string(""),
      id: this.attr(null),
      includeRestricted: this.boolean(false),
      isLocal: this.boolean(false),
      isRequired: this.boolean(false),
      isUnique: this.boolean(false),
      label: this.string(""),
      name: this.string(""),
      overrideDescription: this.string(""),
      overrideLabel: this.string(""),
      // foreign key
      entity: this.string(""),
    };
  }

  static piniaExtend = {
    persist: true,
  };
}
