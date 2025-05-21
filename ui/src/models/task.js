import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";
import { Dialog } from "quasar";
import { defineAsyncComponent, ref } from "vue";

import { requests } from "@/api";
import { CustomModel, CustomRepository, TaskLists, Users } from "@/models";
import { taskSchema, tasksSchema } from "@/schemas";
import { useAuthStore } from "@/stores/auth";
import { isObject } from "@/utils";

class Task extends CustomModel {
  static entity = "task";
  static requests = requests.tasks;
  static schema = {
    instance: taskSchema,
    list: tasksSchema,
  };

  static piniaOptions = {
    ready: ref(false),
    totalCounts: ref({ all: 0, user: 0, created: 0, assigned: 0, completed: 0 }),
    showCounts: ref({ all: 5, created: 5, assigned: 5, completed: 5 }),
    current: ref(null),
    activeFilters: ref(new Set()),
    activeSort: ref(""),
  };

  static autoFields = {
    creationUserId: Users,
    modificationUserId: Users,
    completedById: Users,
    assigneeIds: Users,
  };

  static fields() {
    return {
      id: this.attr(null),
      title: this.string(""),
      taskListId: this.attr(null),
      description: this.string(""),
      priority: this.number(0),
      dueDate: this.attr(null),
      completed: this.boolean(false),
      completedDate: this.attr(null),
      url: this.string(""),
      completedById: this.attr(null),
      files: this.attr([]),
      resources: this.attr([]),
      assigneeIds: this.attr(null),
      commentCount: this.number(0),
      overdue: this.boolean(false),
      creationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      modificationTimestamp: this.attr(null),
      modificationUserId: this.attr(null),
      // related
      taskList: this.belongsTo(TaskLists, "taskListId"),
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      completedBy: this.belongsTo(Users, "completedById"),
      assignees: this.hasManyBy(Users, "assigneeIds"),
    };
  }
  static casts() {
    return {
      completedDate: DateCast,
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }

  get auth() {
    return useAuthStore();
  }
  get completedByAuthor() {
    return this.completed && this.completedById == this.creationUserId;
  }
  get isAuthor() {
    return this.auth.user.id == this.creationUserId;
  }
  get isAssignee() {
    return this.assigneeIds.includes(this.auth.user.id);
  }
  get isTeamMember() {
    return this.taskList.teamLinkId && this.auth.user.groupIds.includes(this.taskList.teamLinkId);
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

class TaskRepo extends CustomRepository {
  use = Task;

  // getters
  get isReady() {
    return this.store.ready;
  }

  get totalCounts() {
    return this.store.totalCounts;
  }

  get showCounts() {
    return this.store.showCounts;
  }

  get activeFilters() {
    return this.store.activeFilters;
  }

  get activeSort() {
    return this.store.activeSort;
  }

  get moreTasks() {
    return this.store.showCounts.all < this.store.totalCount;
  }

  get moreAssigned() {
    return this.store.showCounts.assigned < this.store.assignedCount;
  }

  get moreCompleted() {
    return this.store.showCounts.completed < this.store.completedCount;
  }

  get moreCreated() {
    return this.store.showCounts.created < this.store.createdCount;
  }

  get assigned() {
    return this.query()
      .withAllRecursive()
      .where("isAssignee", true)
      .limit(this.store.showCounts.assigned)
      .get();
  }

  get completed() {
    return this.query()
      .withAllRecursive()
      .where("completed", true)
      .limit(this.store.showCounts.completed)
      .get();
  }

  get created() {
    return this.query()
      .withAllRecursive()
      .where((q) => q.isAuthor === true && q.isAssignee === false && q.completed === false)
      .limit(this.store.showCounts.created)
      .get();
  }

  get listGroups() {
    return this.query().withAllRecursive().groupBy("teamLink.name").get();
  }

  get loadedCounts() {
    return {
      all: this.query().all().length,
      assigned: this.assigned.length,
      completed: this.completed.length,
      created: this.created.length,
    };
  }

  get current() {
    return this.store.current;
  }

  // setters
  set current(task) {
    this.store.current = task;
  }

  // overrides
  processResponse(response) {
    this.totalCounts.all = response.totalTasks;
    this.totalCounts.user = response.count;
    this.totalCounts.created = response.totalCreated;
    this.totalCounts.assigned = response.totalAssigned;
    this.totalCounts.completed = response.totalCompleted;
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
    console.log("remoteListByUser", userId, this);
    return this.remoteCall(this.requests.getByUser(userId), this.schema.list);
  }

  remoteListAssigned(userId) {
    return this.remoteCall(this.requests.getAssigned(userId), this.schema.list);
  }

  remoteListCompleted(userId) {
    return this.remoteCall(this.requests.getCompleted(userId), this.schema.list);
  }

  remoteListCreated(userId) {
    return this.remoteCall(this.requests.getCreated(userId), this.schema.list);
  }

  onShowMore(type) {
    let target =
      this.showCounts[type] + 1 >= this.totalCounts[type]
        ? this.totalCounts[type]
        : (this.showCounts[type] += 1);

    if (target > this.loadedCounts[type] && this.loadedCounts[type] < this.totalCounts[type]) {
      console.log("onShowMore", type, target, this.totalCounts[type], this.loadedCounts[type]);
      // fetchData(Tasks, "task", type, 1, this.loadedCounts[type]).then(() => {
      //   this.showCounts.value[type] = target;
      // });
    }
  }

  onChangeStatus(evt) {
    console.log("onChangeStatus", evt);
  }

  setCurrent(task) {
    this.current = isObject(task) ? task.id : task;
  }

  showModal() {
    Dialog.create({
      component: defineAsyncComponent(() => import("components/task-manager/TaskViewer.vue")),
    });
  }

  clearFilters() {
    this.store.activeFilters.clear();
  }
}

export const Tasks = useRepo(TaskRepo);
