import { Model } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { useAuthStore } from "@/stores/auth";

export default class Task extends Model {
  static entity = "task";

  static fields() {
    return {
      id: this.attr(null),
      title: this.string(""),
      taskList: this.attr(null),
      description: this.string(""),
      priority: this.number(0),
      dueDate: this.attr(null),
      completed: this.boolean(false),
      completedDate: this.attr(null),
      url: this.string(""),
      completedBy: this.attr(null),
      files: this.attr([]),
      resources: this.attr([]),
      assignees: this.attr([]),
      commentCount: this.number(0),
      overdue: this.boolean(false),
      creationTimestamp: this.attr(null),
      creationUser: this.attr(null),
      modificationTimestamp: this.attr(null),
      modificationUser: this.attr(null),
    };
  }
  static casts() {
    return {
      completedDate: DateCast,
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }

  static piniaOptions = {
    persist: true,
  };

  get auth() {
    return useAuthStore();
  }
  get assigneeIds() {
    return Array.from(this.assignees, (i) => i.id);
  }
  get completedByAuthor() {
    return this.completed && this.completedBy.id == this.creationUser.id;
  }
  get isAuthor() {
    return this.auth.user.userId == this.creationUser.id;
  }
  get isAssignee() {
    return this.assigneeIds.includes(this.auth.user.userId);
  }
  get isTeamMember() {
    return this.taskList.teamLink && this.auth.user.groups.includes(this.taskList.teamLink.name);
  }
  get canChange() {
    return this.isAuthor || this.isAssignee || this.isTeamMember;
  }
  get listSlug() {
    if (!this.taskList) {
      return this.creationUser.username;
    } else {
      const groupLabel = this.taskList.teamLink
        ? this.taskList.teamLink.name
        : this.creationUser.username;
      return `${groupLabel}-${this.taskList.name}`;
    }
  }
}
