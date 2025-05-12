import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { requests } from "@/api";
import {
  Agents,
  Attributes,
  Collections,
  CustomModel,
  CustomRepository,
  Places,
  Users,
} from "@/models";
import { recordDetailSchema, recordListSchema } from "@/schemas";

import { Pages } from "./page";
import { Workflows } from "./workflow";

class Record extends CustomModel {
  static entity = "record";
  static requests = requests.records;
  static schema = {
    instance: recordDetailSchema,
    list: recordListSchema,
  };

  static autoFields = {
    agentIds: Agents,
    attributeIds: Attributes,
    creationUserId: Users,
    modificationUserId: Users,
    ownerId: Users,
    collectionIds: Collections,
    placeIds: Places,
  };

  static fields() {
    return {
      agentIds: this.attr([]),
      attributeIds: this.attr([]),
      collectionIds: this.attr([]),
      commentCount: this.number(0),
      creationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      creditLine: this.string(""),
      id: this.attr(null),
      isPrivate: this.boolean(false),
      modificationTimestamp: this.attr(null),
      modificationUserId: this.attr(null),
      name: this.string(""),
      noFolios: this.number(0),
      noTranscriptions: this.number(0),
      ownerId: this.attr(null),
      pages: this.hasMany(Pages, "recordId"),
      parent: this.attr(null),
      permissions: this.attr(null),
      placeIds: this.attr([]),
      shortName: this.string(""),
      workflow: this.hasOne(Workflows, "record"),
      // related
      agents: this.hasManyBy(Agents, "agentIds"),
      attributes: this.hasManyBy(Attributes, "attributeIds"),
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      owner: this.belongsTo(Users, "ownerId"),
      collections: this.hasManyBy(Collections, "collectionIds"),
      places: this.hasManyBy(Places, "placeIds"),
    };
  }

  static casts() {
    return {
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }

  static saving(model, record) {
    console.log("triggered SAVING", model, record);
  }

  static updating(model, record) {
    console.log("triggered UPDATING", model, record);
  }

  static saved(model) {
    console.log("triggered SAVED", model);
  }

  static updated(model) {
    console.log("triggered UPDATED", model);
  }

  attr(name) {
    const result = this.attributes.filter((x) => x.name === name);
    if (result.length > 1) return result;
    if (result.length === 1) return result[0];
    return null;
  }
}

class RecordRepo extends CustomRepository {
  use = Record;
}

export const Records = useRepo(RecordRepo);
