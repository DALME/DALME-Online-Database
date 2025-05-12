import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { requests } from "@/api";
import { Attributes, CustomModel, CustomRepository, Groups, Users } from "@/models";
import { collectionSchema, collectionsSchema } from "@/schemas";

class Collection extends CustomModel {
  static entity = "collection";
  static requests = requests.collections;
  static schema = {
    instance: collectionSchema,
    list: collectionsSchema,
  };

  static autoFields = {
    creationUserId: Users,
    modificationUserId: Users,
    ownerId: Users,
    teamLinkId: Groups,
    attributeIds: Attributes,
  };

  static fields() {
    return {
      id: this.attr(null),
      name: this.string(""),
      attributeIds: this.attr([]),
      useAsWorkset: this.boolean(false),
      isPublished: this.boolean(false),
      isPrivate: this.boolean(false),
      ownerId: this.attr(null),
      teamLinkId: this.attr(null),
      creationTimestamp: this.attr(null),
      modificationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      modificationUserId: this.attr(null),
      memberCount: this.number(0),
      commentCount: this.number(0),
      // related
      owner: this.belongsTo(Users, "ownerId"),
      teamLink: this.belongsTo(Groups, "teamLinkId"),
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      attributes: this.hasManyBy(Attributes, "attributeIds"),
    };
  }

  static casts() {
    return {
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }
}

class CollectionRepo extends CustomRepository {
  use = Collection;
}

export const Collections = useRepo(CollectionRepo);
