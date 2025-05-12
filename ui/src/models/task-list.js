import { useRepo } from "pinia-orm";
import { ref } from "vue";

import { requests } from "@/api";
import { CustomModel, CustomRepository, Groups, Tasks, Users } from "@/models";
import { taskListSchema, taskListsSchema } from "@/schemas";

class TaskList extends CustomModel {
  static entity = "task-list";
  static requests = requests.taskLists;
  static schema = {
    instance: taskListSchema,
    list: taskListsSchema,
  };

  static piniaOptions = {
    ready: ref(false),
    activeGroups: ref(new Set()),
    activeLists: ref(new Set()),
  };

  static autoFields = {
    creationUserId: Users,
    modificationUserId: Users,
    ownerId: Users,
    teamLinkId: Groups,
  };

  static fields() {
    return {
      creationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      description: this.string(""),
      id: this.attr(null),
      modificationTimestamp: this.attr(null),
      modificationUserId: this.attr(null),
      name: this.string(""),
      ownerId: this.attr(null),
      slug: this.string(""),
      taskCount: this.number(0),
      teamLinkId: this.attr(null),
      // related
      tasks: this.hasMany(Tasks, "taskListId"),
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      owner: this.belongsTo(Users, "ownerId"),
      teamLink: this.belongsTo(Groups, "teamLinkId"),
    };
  }
}

class TaskListRepo extends CustomRepository {
  use = TaskList;

  // getters
  get isReady() {
    return this.store.ready;
  }

  get activeGroups() {
    return this.store.activeGroups;
  }

  get activeLists() {
    return this.store.activeLists;
  }

  // overrides
  processResponse(response) {
    return response.data;
  }

  // actions
  init(userId) {
    if (this.store.ready) return Promise.resolve();
    return new Promise((resolve) => {
      this.remoteListByUser(userId).then(() => {
        this.store.ready = true;
        resolve();
      });
    });
  }

  remoteListByUser(userId) {
    return this.remoteCall(this.requests.getByUser(userId), this.schema.list);
  }

  clearListFilters() {
    this.store.activeGroups.clear();
    this.store.activeLists.clear();
  }

  setFilterList(value, isGroup = false) {
    if (isGroup) {
      if (this.activeGroups.has(value)) {
        this.store.activeGroups.delete(value);
        this.query()
          .all()
          .index[value].forEach((x) => this.store.activeLists.delete(`${value}-${x}`));
      } else {
        this.store.activeGroups.add(value);
        this.query()
          .all()
          .index[value].forEach((x) => this.storeactiveLists.value.add(`${value}-${x}`));
      }
    } else {
      if (this.activeLists.has(value)) {
        this.store.activeLists.delete(value);
      } else {
        this.store.activeLists.value.add(value);
      }
    }
  }
}

export const TaskLists = useRepo(TaskListRepo);
