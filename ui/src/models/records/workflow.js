import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { CustomModel, CustomRepository, Users } from "@/models";

import { Logs } from "./log";

class Workflow extends CustomModel {
  static entity = "workflow";
  static primaryKey = "record";

  static autoFields = {
    lastUserId: Users,
  };

  static fields() {
    return {
      helpFlag: this.boolean(false),
      ingestionDone: this.boolean(false),
      isPublic: this.boolean(false),
      lastModified: this.attr(null),
      lastUserId: this.attr(null),
      markupDone: this.boolean(false),
      parsingDone: this.boolean(false),
      record: this.attr(null),
      reviewDone: this.boolean(false),
      stage: this.number(0),
      status: this.string(""),
      transcriptionDone: this.boolean(false),
      wfStatus: this.number(0),
      workLog: this.hasMany(Logs, "record"),
      // related
      lastUser: this.belongsTo(Users, "lastUserId"),
    };
  }
  static casts() {
    return {
      lastModified: DateCast,
    };
  }
}

class WorkflowRepo extends CustomRepository {
  use = Workflow;
}

export const Workflows = useRepo(WorkflowRepo);
