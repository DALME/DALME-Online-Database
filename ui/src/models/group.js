import { useRepo } from "pinia-orm";

import { requests } from "@/api";
import { CustomModel, CustomRepository } from "@/models";
import { groupAttributeSchema, groupListSchema } from "@/schemas";

class Group extends CustomModel {
  static entity = "group";
  static requests = requests.groups;
  static schema = {
    instance: groupAttributeSchema,
    list: groupListSchema,
  };

  static fields() {
    return {
      description: this.string(""),
      groupType: this.string(""),
      id: this.attr(null),
      name: this.string(""),
    };
  }
}

class GroupRepo extends CustomRepository {
  use = Group;
}

export const Groups = useRepo(GroupRepo);
