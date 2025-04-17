import { Model } from "pinia-orm";
import Task from "./task";

export default class TaskList extends Model {
  static entity = "task-list";

  static fields() {
    return {
      id: this.attr(null),
      name: this.string(""),
      slug: this.string(""),
      description: this.string(""),
      teamLink: this.attr(null),
      owner: this.attr(null),
      taskCount: this.number(0),
      creationTimestamp: this.attr(null),
      creationUser: this.attr(null),
      modificationTimestamp: this.attr(null),
      modificationUser: this.attr(null),
      tasks: this.hasMany(Task, "taskList"),
    };
  }

  static piniaOptions = {
    persist: true,
  };
}
