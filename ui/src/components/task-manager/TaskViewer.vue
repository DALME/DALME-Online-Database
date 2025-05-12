<template>
  <q-dialog
    ref="dialogRef"
    @hide="onDialogHide"
    class="frosted-background dialogue-top"
    transition-hide="scale"
    transition-show="scale"
    no-esc-dismiss
  >
    <div :class="fullHeight ? 'action-modal-card full-height' : 'action-modal-card'">
      <div :class="openDrawer ? 'show' : ''" class="card-drawer">
        <template v-if="openDrawer">
          <div class="q-mb-md">
            <div
              v-if="
                !nully(Tasks.listGroups) || Tasks.all().length > 0 || Tasks.totalCounts.user > 0
              "
              class="tasklist-toolbar"
            >
              <TasklistManager v-if="!nully(Tasks.listGroups)" :lists="Tasks.listGroups" />
              <template v-if="Tasks.all().length > 0 || Tasks.totalCounts.user > 0">
                <q-btn-dropdown
                  content-class="popup-menu filtered dark info-list menu-only"
                  label="Filter"
                  menu-anchor="bottom left"
                  menu-self="top left"
                  size="12px"
                >
                  <q-list separator>
                    <q-item class="header" dense>
                      <q-item-section>Status</q-item-section>
                      <q-item-section side>
                        <q-btn @click.stop="Tasks.clearFilters" icon="close" size="xs" dense flat />
                      </q-item-section>
                    </q-item>
                    <q-item v-close-popup class="inset-item" clickable dense>
                      <q-item-section>Completed</q-item-section>
                    </q-item>
                    <q-item v-close-popup class="inset-item" clickable dense>
                      <q-item-section>Overdue</q-item-section>
                    </q-item>
                    <q-item v-close-popup class="inset-item" clickable dense>
                      <q-item-section>Pending</q-item-section>
                    </q-item>
                    <q-item class="header" dense>
                      <q-item-section>Users</q-item-section>
                    </q-item>
                    <q-item v-close-popup class="inset-item" clickable dense>
                      <q-item-section>Created by</q-item-section>
                    </q-item>
                    <q-item v-close-popup class="inset-item" clickable dense>
                      <q-item-section>Completed by</q-item-section>
                    </q-item>
                    <GeneralChooser
                      @item-chosen="$emit('userSelected')"
                      label="Author"
                      return-field="username"
                      type="users"
                      dark
                      item
                    />
                  </q-list>
                </q-btn-dropdown>
                <q-btn-dropdown
                  content-class="popup-menu filtered dark info-list menu-only"
                  label="Sort"
                  menu-anchor="bottom left"
                  menu-self="top left"
                  size="12px"
                >
                  <q-list separator>
                    <q-item class="header" dense>
                      <q-item-section>Sort by</q-item-section>
                      <q-item-section side>
                        <q-btn
                          @click.stop="Tasks.activeSort == ''"
                          icon="close"
                          size="xs"
                          dense
                          flat
                        />
                      </q-item-section>
                    </q-item>
                    <q-item
                      v-for="(item, idx) in sortMenu"
                      :key="idx"
                      v-close-popup
                      @click.stop="Tasks.activeSort == item.value"
                      :active="item.value == Tasks.activeSort"
                      class="inset-item"
                      clickable
                      dense
                    >
                      <q-item-section>{{ item.label }}</q-item-section>
                    </q-item>
                  </q-list>
                </q-btn-dropdown>
                <q-btn icon="mdi-magnify" />
              </template>
            </div>
          </div>
          <q-scroll-area class="scroll-area" dark>
            <TaskList
              @change-status="Tasks.onChangeStatus"
              @show-more="Tasks.onShowMore('all')"
              @view-detail="Tasks.setCurrent"
              :data="Tasks.all()"
              :more-button="Tasks.moreTasks"
              :no-data-message="noTasksData"
              :scroll-off="Tasks.current == null"
            />
          </q-scroll-area>
        </template>
      </div>
      <div class="separator" />
      <div class="card-main">
        <div :class="Tasks.current ? 'task-wrapper border' : 'task-wrapper'">
          <q-item class="task-title">
            <q-item-section avatar>
              <q-btn
                @click="openDrawer = !openDrawer"
                :color="openDrawer ? 'deep-purple-4' : 'blue-grey-7'"
                :icon="openDrawer ? 'mdi-list-box' : 'mdi-list-box-outline'"
                :icon-right="openDrawer ? 'mdi-menu-left' : 'mdi-menu-right'"
                class="q-pa-none"
                dense
                flat
              />
            </q-item-section>
            <q-item-section v-if="Tasks.current">
              <q-item-label>
                {{ task.title }}
                <q-chip
                  :color="taskStatus[2]"
                  :icon="taskStatus[0]"
                  :label="taskStatus[1]"
                  class="q-ml-md"
                  size="12px"
                  text-color="white"
                />
              </q-item-label>
              <q-item-label caption>
                <span v-text="`Created ${formatDate(task.creationTimestamp, 'DATETIME_AT')} by `" />
                <DetailPopover :user-data="task.creationUser" dark show-avatar />
                <template v-if="task.completed">
                  <span
                    v-text="`, completed ${formatDate(task.completedDate, 'DATETIME_AT')} by `"
                  />
                  <DetailPopover :user-data="task.completedBy" dark show-avatar />
                </template>
              </q-item-label>
            </q-item-section>
            <q-item-section class="q-ml-auto" side top>
              <q-btn v-close-popup icon="mdi-close" dense flat round />
            </q-item-section>
          </q-item>
          <template v-if="Tasks.current">
            <q-item class="task-container">
              <q-item-section avatar top>
                <q-icon name="mdi-note-outline" />
              </q-item-section>
              <q-item-section>
                <MarkdownEditor v-if="task.description" :text="task.description" dark />
                <span v-else>No description provided.</span>
              </q-item-section>
              <q-item-section side top>
                <div class="task-meta">
                  <div v-if="task.assignees.length">
                    <div class="meta-label">Assignees</div>
                    <div class="meta-content">
                      <q-avatar v-for="(user, i) in task.assignees" :key="i" size="30px">
                        <q-img
                          v-if="!nully(user.avatar)"
                          :src="user.avatar"
                          fit="cover"
                          ratio="1"
                        />
                        <q-icon v-else name="mdi-account-circle" size="28px" />
                      </q-avatar>
                    </div>
                  </div>
                  <div v-if="task.files.length">
                    <div class="meta-label">Attachments</div>
                    <div class="meta-content">
                      <AttachmentWidget
                        v-for="(file, i) in task.files"
                        :key="i"
                        :file="file"
                        compact
                        icon-only
                      />
                    </div>
                  </div>
                  <div v-if="task.resources.length">
                    <div class="meta-label">Resources</div>
                  </div>
                </div>
              </q-item-section>
            </q-item>
            <div class="task-footer">
              <div v-if="task.dueDate" class="text-caption">
                <q-btn @click="changeDueDate" icon="mdi-calendar-edit-outline" dense flat />
                <span v-text="`Due on ${formatDate(task.dueDate, 'DATE_MED_WITH_WEEKDAY')} `" />
              </div>
              <q-btn v-if="task.url" @click="openURL(task.url)" icon="mdi-link" flat />
              <q-btn
                v-if="task.canChange"
                @click.stop="onAction"
                :class="`action-button ${action[1]}`"
                :label="capitalize(action[0])"
                flat
              />
            </div>
          </template>
          <div v-else class="no-task-data">
            <q-spinner-bars class="q-mb-lg" color="blue-grey-9" size="xl" />
            <div class="text-weight-medium text-blue-grey-6">
              Select a task to display its information here.
            </div>
          </div>
        </div>
        <q-scroll-area v-if="Tasks.current" class="scroll-area q-px-lg" dark>
          <CommentBox :author="task.creationUser.id" dark>
            <template v-if="task.completed" #comment-stream-end>
              <q-item :class="task.completedByAuthor ? 'op-post' : ''" class="comment-box">
                <q-item-section v-if="task.completedByAuthor" avatar>
                  <q-avatar class="closing-dot" size="40px">
                    <q-icon color="white" name="mdi-check-circle" size="20px" />
                  </q-avatar>
                </q-item-section>
                <q-item-section :style="!task.completedByAuthor ? 'align-content: end;' : ''">
                  <span v-text="`completed ${formatDate(task.completedDate, 'DATETIME_AT')} by `" />
                  <DetailPopover :user-data="task.completedBy" dark show-avatar />
                </q-item-section>
                <q-item-section v-if="!task.completedByAuthor" side>
                  <q-avatar class="closing-dot" size="40px">
                    <q-icon color="white" name="mdi-check-circle" size="20px" />
                  </q-avatar>
                </q-item-section>
              </q-item>
            </template>
          </CommentBox>
        </q-scroll-area>
      </div>
    </div>
  </q-dialog>
</template>

<script>
import { format, openURL, useDialogPluginComponent } from "quasar";
import { computed, onMounted, provide, ref, watch } from "vue";

import {
  AttachmentWidget,
  CommentBox,
  DetailPopover,
  GeneralChooser,
  MarkdownEditor,
} from "@/components";
import { Tasks } from "@/models";
import { useAuthStore } from "@/stores/auth";
import { formatDate, nully } from "@/utils";

import TaskList from "./TaskList.vue";
import TasklistManager from "./TasklistManager.vue";

export default {
  components: {
    AttachmentWidget,
    CommentBox,
    DetailPopover,
    MarkdownEditor,
    TasklistManager,
    TaskList,
    GeneralChooser,
  },
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide } = useDialogPluginComponent();
    const auth = useAuthStore();
    const { capitalize } = format;
    const openDrawer = ref(false);
    const attachment = ref(null);
    const id = computed(() => (Tasks.current ? Tasks.current : null));
    const task = ref(null);

    const action = computed(() =>
      id.value ? (task.value.completed ? ["mark pending", "open"] : ["mark done", "close"]) : null,
    );

    const taskStatus = computed(() => {
      if (id.value) {
        let label = task.value.completed ? "DONE" : "PENDING";
        let colour = task.value.completed ? "light-green-9" : "deep-purple-6";
        let icon = task.value.completed ? "mdi-check-circle" : "mdi-dots-horizontal-circle-outline";
        return task.value.overdue == true
          ? ["mdi-clock-alert-outline", "OVERDUE", "red-5"]
          : [icon, label, colour];
      } else {
        return null;
      }
    });

    const fullHeight = computed(() => {
      if (id.value) {
        return (openDrawer.value && Tasks.all().length > 5) || task.value.commentCount > 0;
      } else {
        return Tasks.all().length > 5;
      }
    });

    const sortMenu = [
      { label: "Newest", value: "" },
      { label: "Oldest", value: "" },
      { label: "Due date", value: "" },
      { label: "Completed date", value: "" },
      { label: "Most commented", value: "" },
      { label: "Least commented", value: "" },
    ];

    const noTasksData = computed(() => {
      if (Tasks.totalCounts.user > 0) {
        return "No tasks match the current filter or search criteria.";
      } else {
        // eslint-disable-next-line max-len
        return "Neither you nor your team have created any tasks yet, and no tasks have yet been assigned to you.";
      }
    });

    const onAction = () => {
      console.log("action");
    };

    const changeDueDate = () => {
      console.log("changeDueDate");
    };

    provide("attachment", attachment);
    provide("model", "Task");
    provide("id", id);

    watch(
      () => id.value,
      () => {
        if (id.value) {
          task.value = Tasks.withAllRecursive().find(id.value);
        }
      },
      { immediate: true },
    );

    onMounted(() => {
      if (!id.value) {
        openDrawer.value = true;
      }
    });

    return {
      action,
      attachment,
      capitalize,
      formatDate,
      dialogRef,
      onDialogHide,
      onAction,
      auth,
      openDrawer,
      taskStatus,
      nully,
      openURL,
      changeDueDate,
      sortMenu,
      fullHeight,
      noTasksData,
      Tasks,
      task,
    };
  },
};
</script>

<style lang="scss" scoped>
@media (max-height: 500px) {
  .dialogue-top .q-dialog__inner {
    padding-top: 20px !important;
    padding-bottom: 20px !important;
  }
  .q-dialog__inner > div.action-modal-card {
    max-height: calc(100vh - 40px) !important;
  }
}
@media (max-width: 1000px) {
  .card-main .task-wrapper {
    min-width: 500px !important;
  }
}
.dialogue-top .q-dialog__inner {
  align-items: flex-start;
  padding: 75px 100px 50px 100px;
}
.q-dialog__inner > div.action-modal-card {
  display: flex;
  flex-direction: row;
  max-width: 1500px;
  padding: 18px 18px 18px 0;
  max-height: calc(100vh - 125px);
  background: var(--dark-bg-base-colour);
  border-radius: 12px;
  border: 1px solid var(--dark-border-base-colour);
  box-shadow: 0 5px 24px 0px rgb(0 0 0 / 48%);
  transition: all 0.2s linear;
  color: var(--dark-default-text-colour);
  // overflow: hidden;
}
.action-modal-card .q-card {
  background: var(--dark-bg-base-colour);
  border-color: var(--dark-border-base-colour);
}
.action-modal-card .q-separator {
  background: var(--dark-border-base-colour);
}
.card-main {
  display: flex;
  flex-direction: column;
  padding-left: 18px;
}
.card-drawer {
  display: flex;
  flex-direction: column;
  width: 0;
  opacity: 0;
  transition: all 0.3s linear;
  border-radius: 0 !important;
  box-shadow:
    1px 0px 0px 0px #1e2a31,
    inset -1px 0px 0px 0px #000000;
  height: auto;
  min-height: 350px;
  flex-shrink: 0;
}
.card-drawer.show {
  width: 350px;
  padding-left: 18px;
  opacity: 1;
  padding-right: 8px;
}
.card-drawer .scroll-area {
  min-height: 250px;
  height: 100%;
}
.card-main .task-wrapper {
  margin-bottom: 24px;
  min-width: 800px;
}
.card-main .task-wrapper.border {
  border-bottom: 1px solid var(--dark-border-base-colour);
}
.card-main .task-wrapper .no-task-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 250px;
}
.card-main .scroll-area {
  min-height: 250px;
  height: 100%;
}
.card-drawer .drawer-menu-list {
  display: block;
  flex-direction: unset;
  width: 316px;
  padding-right: 8px;
}
.task-title {
  padding: 0 0 15px 5px;
  border-bottom: 1px solid var(--dark-border-base-colour);
  min-height: unset;
}
.task-title .q-item__section--main {
  flex-wrap: nowrap;
}
.task-title .q-item__section--main .q-item__label {
  display: flex;
  align-items: center;
}
.task-title .q-item__section--main .q-item__label:not(.q-item__label--caption) {
  color: var(--dark-text-accent);
  font-size: 22px;
}
.task-title .q-item__section--main .q-item__label--caption {
  color: var(--dark-secondary-text-colour);
  font-size: 14px;
  white-space: break-spaces;
}
.task-title .q-item__section--avatar {
  justify-content: flex-end;
  padding-right: 8px;
  margin-right: 16px;
  border-right: 1px solid var(--dark-border-base-colour) !important;
}
.task-title .q-item__section--avatar .q-btn {
  width: 32px;
}
.task-container {
  padding: 30px 0 16px 16px;
  margin: 0 43px;
  min-height: unset;
}
.task-container .q-item__section--main {
  justify-content: flex-start;
}
.task-container .q-item__section--avatar {
  padding: 2px 10px 0 0;
}
.task-container .q-item__section--avatar .q-icon {
  font-size: 19px;
  color: var(--dark-secondary-text-colour);
}
.task-footer {
  display: flex;
  height: 30px;
  margin: 0 43px;
  padding: 0;
  border: 1px solid var(--dark-border-base-colour);
  background-color: var(--dark-bg-raised-colour);
  margin-bottom: 24px;
  border-radius: 8px;
}
.task-footer .q-btn {
  color: var(--dark-secondary-text-colour);
  padding: 0.285em;
  min-height: 2em;
}
.task-footer > .q-btn:not(.action-button) {
  font-size: 12px;
  height: 28px;
  width: 38px;
  border-radius: 0;
  border-right: 1px solid var(--dark-border-base-colour);
}
.task-footer > div {
  display: flex;
  align-items: center;
  white-space: break-spaces;
  border-right: 1px solid var(--dark-border-base-colour);
  padding-right: 16px;
}
.task-footer > div .q-btn {
  font-size: 9px;
  margin-right: 3px;
  margin-left: 14px;
}
.task-footer .action-button {
  margin-left: auto;
  border-radius: 0 8px 8px 0;
  padding: 0 16px;
  border-left: 1px solid var(--dark-border-base-colour);
  font-size: 12px;
}
.task-footer .action-button.open {
  color: var(--dark-indigo-button-text);
  background-color: var(--dark-indigo-button-bg);
}
.task-footer .action-button.close {
  color: var(--dark-green-button-text);
  background-color: var(--dark-green-button-bg);
}
.task-meta {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.task-meta > div {
  display: flex;
  border: 1px solid var(--dark-border-base-colour);
  border-radius: 8px;
  padding: 6px 12px;
  align-items: center;
  gap: 10px;
  background-color: var(--dark-bg-raised-colour);
}
.task-meta > div .meta-content {
  display: flex;
  gap: 10px;
}
.task-meta > div .meta-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--dark-secondary-text-colour);
}
.task-meta > div .meta-content .q-icon {
  font-size: 30px;
  color: var(--dark-secondary-text-colour);
}
.tasklist-toolbar {
  display: flex;
  background: var(--dark-bg-raised-colour);
  border: 1px solid var(--dark-border-base-colour);
  border-radius: 8px;
  margin-right: 16px;
}
.tasklist-toolbar > .q-btn {
  border: none;
  border-radius: 0;
  padding: 0 10px 0 16px;
  text-transform: none;
  border-right: 1px solid var(--dark-menu-separator);
}
.tasklist-toolbar > .q-btn::before {
  box-shadow: none;
}
.tasklist-toolbar > .q-btn:first-of-type {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  border-left: none;
}
.tasklist-toolbar > .q-btn:last-of-type {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  width: 100%;
  padding: 0;
  font-size: 11px;
}
.tasklist-toolbar .q-btn-dropdown__arrow {
  margin-left: 4px;
}
.info-list .q-item.q-hoverable:hover {
  color: var(--dark-text-accent) !important;
}
.menu-only > .q-list {
  min-width: unset !important;
}
.menu-only > .q-list .q-item.inset-item {
  padding-right: 40px !important;
}
.scrollarea-off {
  position: static;
  contain: none;
}
.scrollarea-off .q-scrollarea__container {
  position: static;
}
.scrollarea-off .q-scrollarea__container .q-scrollarea__content {
  position: static;
}
</style>
