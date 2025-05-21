import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { CustomModel, CustomRepository, Users } from "@/models";

class Log extends CustomModel {
  static entity = "log";
  static autoFields = {
    userId: Users,
  };

  static fields() {
    return {
      record: this.attr(null),
      event: this.string(""),
      id: this.number(null),
      timestamp: this.attr(null),
      userId: this.attr(null),
      // related
      user: this.belongsTo(Users, "userId"),
    };
  }
  static casts() {
    return {
      timestamp: DateCast,
    };
  }
}

class LogRepo extends CustomRepository {
  use = Log;
}

export const Logs = useRepo(LogRepo);
