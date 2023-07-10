import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { API as apiInterface, requests } from "@/api";
import { useAuthStore } from "@/stores/auth";
import { tasksSchema } from "@/schemas";

class Task {
  constructor(data, user, groups) {
    this.currentUserId = user;
    this.currentUserGroups = groups;
    this.id = data.id;
    this.title = data.title;
    this.taskList = data.taskList;
    this.description = data.description;
    this.dueDate = data.dueDate;
    this.completed = data.completed;
    this.completedDate = data.completedDate;
    this.completedBy = data.completedBy;
    this.overdue = data.overdue;
    this.files = data.files;
    this.resources = data.resources;
    this.assignees = data.assignees;
    this.url = data.url;
    this.commentCount = data.commentCount;
    this.creationTimestamp = data.creationTimestamp;
    this.creationUser = data.creationUser;
    this.modificationTimestamp = data.modificationTimestamp;
    this.modificationUser = data.modificationUser;
  }
  // getters
  get assigneeIds() {
    return Array.from(this.assignees, (i) => i.id);
  }
  get completedByAuthor() {
    return this.completed && this.completedBy.id == this.creationUser.id;
  }
  get isAuthor() {
    return this.currentUserId == this.creationUser.id;
  }
  get isAssignee() {
    return this.assigneeIds.includes(this.currentUserId);
  }
  get isTeamMember() {
    return this.taskList.teamLink && this.currentUserGroups.includes(this.taskList.teamLink.name);
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
  // methods
  // isAuthor = (id) => id == this.creationUser.id;
  // isAssignee = (id) => this.assigneeIds.includes(id);
  // isTeamMember = (groups) => this.taskList.teamLink
  //&& groups.includes(this.taskList.teamLink.name);
  // canChange = (id, groups) => this.isAuthor(id) || this.isAssignee(id)
  //|| this.isTeamMember(groups);
}

export const useTaskStore = defineStore("taskStore", () => {
  // stores
  const auth = useAuthStore();

  // state
  const tasks = ref([]);
  const timestamp = ref(null);
  const loading = ref(false);
  const meta = ref({
    all: 0,
    user: 0,
    created: 0,
    assigned: 0,
    completed: 0,
  });

  // getters
  const _isStale = computed(() => Date.now() - timestamp.value > 86400000);
  const isLoaded = computed(() => tasks.value.length && auth.userId);

  // actions
  const $reset = () => {
    tasks.value = [];
    timestamp.value = null;
    loading.value = false;
    meta.value = {
      all: 0,
      user: 0,
      created: 0,
      assigned: 0,
      completed: 0,
    };
  };

  const init = () => {
    $reset();
    fetchData("user", 15);
  };

  const getRequest = (type, limit, offset, query) => {
    if (type == "assigned") return requests.tasks.getAssignedTasks(auth.userId, limit, offset);
    if (type == "completed") return requests.tasks.getCompletedTasks(auth.userId, limit, offset);
    if (type == "created") return requests.tasks.getCreatedTasks(auth.userId, limit, offset);
    if (type == "user") return requests.tasks.getUserTasks(auth.userId, limit, offset);
    return requests.tasks.getTasks(query, limit, offset);
  };

  const fetchData = (type, limit, offset = 0, query = null) => {
    return new Promise((resolve) => {
      const { success, data, fetchAPI } = apiInterface();
      loading.value = true;
      fetchAPI(getRequest(type, limit, offset, query)).then(() => {
        if (success.value) {
          tasksSchema.validate(data.value.data, { stripUnknown: true }).then((validatedData) => {
            timestamp.value = Date.now();
            if (!isLoaded.value) {
              meta.value = {
                all: data.value.totalTasks,
                user: data.value.count,
                created: data.value.totalCreated,
                assigned: data.value.totalAssigned,
                completed: data.value.totalCompleted,
              };
            }
            validatedData.forEach((x) => tasks.value.push(new Task(x, auth.userId, auth.groups)));
            loading.value = false;
            return resolve;
          });
        }
      });
    });
  };

  return {
    init,
    $reset,
    isLoaded,
    loading,
    tasks,
    meta,
    fetchData,
  };
});
