import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { requests } from "@/api";
import { CustomModel, CustomRepository, Groups } from "@/models";
import { userListSchema, userSchema } from "@/schemas";

class User extends CustomModel {
  static entity = "user";
  static requests = requests.users;
  static schema = {
    instance: userSchema,
    list: userListSchema,
  };

  static autoFields = {
    groupIds: Groups,
  };

  static fields() {
    return {
      avatar: this.string(""),
      dateJoined: this.attr(null),
      email: this.string(""),
      firstName: this.string(""),
      fullName: this.string(""),
      groupIds: this.attr([]),
      id: this.attr(null),
      isActive: this.boolean(false),
      isStaff: this.boolean(false),
      isSuperuser: this.boolean(false),
      lastLogin: this.attr(null),
      lastName: this.string(""),
      username: this.string(""),
      // related
      groups: this.hasManyBy(Groups, "groupIds"),
    };
  }

  static casts() {
    return {
      dateJoined: DateCast,
      lastLogin: DateCast,
    };
  }
}

class UserRepo extends CustomRepository {
  use = User;
}

export const Users = useRepo(UserRepo);

window.testUserRepo = Users;
