<template>
  <q-dialog
    ref="dialogRef"
    no-esc-dismiss
    transition-show="scale"
    transition-hide="scale"
    class="frosted-background dialogue-top"
    @hide="onDialogHide"
  >
    <div :class="fullHeight ? 'action-modal-card full-height' : 'action-modal-card'">
      <div class="card-drawer" :class="openDrawer ? 'show' : ''">
        <template v-if="openDrawer && tm.listsReady">
          <div class="q-mb-md">
            <div
              v-if="!nully(tm.listGroups) || tm.tasks.length > 0 || tm.tasksMeta.user > 0"
              class="tasklist-toolbar"
            >
              <TasklistManager v-if="!nully(tm.listGroups)" :lists="tm.listGroups" />
              <template v-if="tm.tasks.length > 0 || tm.tasksMeta.user > 0">
                <q-btn-dropdown
                  label="Filter"
                  size="12px"
                  menu-anchor="bottom left"
                  menu-self="top left"
                  content-class="popup-menu filtered dark info-list menu-only"
                >
                  <q-list separator>
                    <q-item dense class="header">
                      <q-item-section>Status</q-item-section>
                      <q-item-section side>
                        <q-btn flat dense size="xs" icon="close" @click.stop="tm.clearFilters" />
                      </q-item-section>
                    </q-item>
                    <q-item dense clickable v-close-popup class="inset-item">
                      <q-item-section>Completed</q-item-section>
                    </q-item>
                    <q-item dense clickable v-close-popup class="inset-item">
                      <q-item-section>Overdue</q-item-section>
                    </q-item>
                    <q-item dense clickable v-close-popup class="inset-item">
                      <q-item-section>Pending</q-item-section>
                    </q-item>
                    <q-item dense class="header">
                      <q-item-section>Users</q-item-section>
                    </q-item>
                    <q-item dense clickable v-close-popup class="inset-item">
                      <q-item-section>Created by</q-item-section>
                    </q-item>
                    <q-item dense clickable v-close-popup class="inset-item">
                      <q-item-section>Completed by</q-item-section>
                    </q-item>
                    <UserChooserWidget
                      item
                      dark
                      return-field="username"
                      label="Author"
                      @item-chosen="$emit('userSelected')"
                    />
                  </q-list>
                </q-btn-dropdown>
                <q-btn-dropdown
                  label="Sort"
                  size="12px"
                  menu-anchor="bottom left"
                  menu-self="top left"
                  content-class="popup-menu filtered dark info-list menu-only"
                >
                  <q-list separator>
                    <q-item dense class="header">
                      <q-item-section>Sort by</q-item-section>
                      <q-item-section side>
                        <q-btn
                          flat
                          dense
                          size="xs"
                          icon="close"
                          @click.stop="tm.activeSort == ''"
                        />
                      </q-item-section>
                    </q-item>
                    <q-item
                      v-for="(item, idx) in sortMenu"
                      :key="idx"
                      dense
                      clickable
                      v-close-popup
                      class="inset-item"
                      :active="item.value == tm.activeSort"
                      @click.stop="tm.activeSort == item.value"
                    >
                      <q-item-section>{{ item.label }}</q-item-section>
                    </q-item>
                  </q-list>
                </q-btn-dropdown>
                <q-btn icon="mdi-magnify" />
              </template>
            </div>
          </div>
          <q-scroll-area dark class="scroll-area">
            <TaskList
              :data="tm.tasks"
              :more-button="tm.moreTasks"
              :no-data-message="noTasksData"
              :scroll-off="tm.viewing == null"
              @show-more="tm.onShowMore('all')"
              @change-status="tm.onChangeStatus"
              @view-detail="tm.setViewing"
            />
          </q-scroll-area>
        </template>
      </div>
      <div class="separator" />
      <div class="card-main">
        <div :class="tm.viewing ? 'task-wrapper border' : 'task-wrapper'">
          <q-item class="task-title">
            <q-item-section avatar>
              <q-btn
                flat
                dense
                class="q-pa-none"
                :icon="openDrawer ? 'mdi-list-box' : 'mdi-list-box-outline'"
                :icon-right="openDrawer ? 'mdi-menu-left' : 'mdi-menu-right'"
                :color="openDrawer ? 'deep-purple-4' : 'blue-grey-7'"
                @click="openDrawer = !openDrawer"
              />
            </q-item-section>
            <q-item-section v-if="tm.viewing">
              <q-item-label>
                {{ tm.viewing.title }}
                <q-chip
                  :icon="taskStatus[0]"
                  :label="taskStatus[1]"
                  :color="taskStatus[2]"
                  text-color="white"
                  size="12px"
                  class="q-ml-md"
                />
              </q-item-label>
              <q-item-label caption>
                <span v-text="`Created ${fDate(tm.viewing.creationTimestamp)} by `" />
                <DetailPopover dark show-avatar :user-data="tm.viewing.creationUser" />
                <template v-if="tm.viewing.completed">
                  <span v-text="`, completed ${fDate(tm.viewing.completedDate)} by `" />
                  <DetailPopover dark show-avatar :user-data="tm.viewing.completedBy" />
                </template>
              </q-item-label>
            </q-item-section>
            <q-item-section top side class="q-ml-auto">
              <q-btn icon="mdi-close" flat round dense v-close-popup />
            </q-item-section>
          </q-item>
          <template v-if="tm.viewing">
            <q-item class="task-container">
              <q-item-section top avatar>
                <q-icon name="mdi-note-outline" />
              </q-item-section>
              <q-item-section>
                <MarkdownEditor v-if="tm.viewing.description" :text="tm.viewing.description" dark />
                <span v-else>No description provided.</span>
              </q-item-section>
              <q-item-section top side>
                <div class="task-meta">
                  <div v-if="tm.viewing.assignees.length">
                    <div class="meta-label">Assignees</div>
                    <div class="meta-content">
                      <q-avatar v-for="(user, i) in tm.viewing.assignees" :key="i" size="30px">
                        <img v-if="!nully(user.avatar)" :src="user.avatar" />
                        <q-icon v-else size="38px" name="mdi-account-circle" />
                      </q-avatar>
                    </div>
                  </div>
                  <div v-if="tm.viewing.files.length">
                    <div class="meta-label">Attachments</div>
                    <div class="meta-content">
                      <AttachmentIconWidget
                        v-for="(file, i) in tm.viewing.files"
                        :key="i"
                        :attachment="file"
                      />
                    </div>
                  </div>
                  <div v-if="tm.viewing.resources.length">
                    <div class="meta-label">Resources</div>
                  </div>
                </div>
              </q-item-section>
            </q-item>
            <div class="task-footer">
              <div v-if="tm.viewing.dueDate" class="text-caption">
                <q-btn flat dense icon="mdi-calendar-edit-outline" @click="changeDueDate" />
                <span v-text="`Due ${fDate(tm.viewing.dueDate, 0, 'h')} `" />
                <span v-text="`(${fDate(tm.viewing.dueDate, 0, 'd', null)})`" />
              </div>
              <q-btn v-if="tm.viewing.url" flat icon="mdi-link" @click="openURL(tm.viewing.url)" />
              <q-btn
                v-if="tm.viewing.canChange"
                flat
                :class="`action-button ${action[1]}`"
                :label="capitalize(action[0])"
                @click.stop="onAction"
              />
            </div>
          </template>
          <div v-else class="no-task-data">
            <q-spinner-bars color="blue-grey-9" size="xl" class="q-mb-lg" />
            <div class="text-weight-medium text-blue-grey-6">
              Select a task to display its information here.
            </div>
          </div>
        </div>
        <q-scroll-area dark class="scroll-area q-px-lg" v-if="tm.viewing">
          <CommentBox dark :author="tm.viewing.creationUser.id">
            <template v-if="tm.viewing.completed" v-slot:comment-stream-end>
              <q-item class="comment-box" :class="tm.viewing.completedByAuthor ? 'op-post' : ''">
                <q-item-section v-if="tm.viewing.completedByAuthor" avatar>
                  <q-avatar size="40px" class="closing-dot">
                    <q-icon name="mdi-check-circle" color="white" size="20px" />
                  </q-avatar>
                </q-item-section>
                <q-item-section :style="!tm.viewing.completedByAuthor ? 'align-content: end;' : ''">
                  <span v-text="`completed ${fDate(tm.viewing.completedDate)} by `" />
                  <DetailPopover dark show-avatar :user-data="tm.viewing.completedBy" />
                </q-item-section>
                <q-item-section v-if="!tm.viewing.completedByAuthor" side>
                  <q-avatar size="40px" class="closing-dot">
                    <q-icon name="mdi-check-circle" color="white" size="20px" />
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
import { useDialogPluginComponent, format, openURL } from "quasar";
import { computed, provide, onMounted, ref } from "vue";
import { formatDate as fDate, nully } from "@/utils";
import { useAuthStore } from "@/stores/auth";
import { useTasks } from "@/stores/tasks";
import TasklistManager from "./TasklistManager.vue";
import TaskList from "./TaskList.vue";
import {
  AttachmentIconWidget,
  CommentBox,
  DetailPopover,
  MarkdownEditor,
  UserChooserWidget,
} from "@/components";

export default {
  components: {
    AttachmentIconWidget,
    CommentBox,
    DetailPopover,
    MarkdownEditor,
    TasklistManager,
    TaskList,
    UserChooserWidget,
  },
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide } = useDialogPluginComponent();
    const auth = useAuthStore();
    const { capitalize } = format;
    const tm = useTasks();
    const openDrawer = ref(false);
    const attachment = ref(null);
    const id = computed(() => (tm.viewing ? tm.viewing.id : null));

    const action = computed(() =>
      tm.viewing
        ? tm.viewing.completed
          ? ["mark pending", "open"]
          : ["mark done", "close"]
        : null,
    );

    const taskStatus = computed(() => {
      if (tm.viewing) {
        let label = tm.viewing.completed ? "DONE" : "PENDING";
        let colour = tm.viewing.completed ? "light-green-9" : "deep-purple-6";
        let icon = tm.viewing.completed ? "mdi-check-circle" : "mdi-dots-horizontal-circle-outline";
        return tm.viewing.overdue == true
          ? ["mdi-clock-alert-outline", "OVERDUE", "red-5"]
          : [icon, label, colour];
      } else {
        return null;
      }
    });

    const fullHeight = computed(() => {
      if (tm.viewing) {
        return (openDrawer.value && tm.tasks.length > 5) || tm.viewing.commentCount > 0;
      } else {
        return tm.tasks.length > 5;
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
      if (tm.tasksMeta.user > 0) {
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

    onMounted(() => {
      if (!tm.viewing) {
        openDrawer.value = true;
      }
    });

    return {
      action,
      attachment,
      capitalize,
      fDate,
      dialogRef,
      onDialogHide,
      onAction,
      auth,
      openDrawer,
      tm,
      taskStatus,
      nully,
      openURL,
      changeDueDate,
      sortMenu,
      fullHeight,
      noTasksData,
    };
  },
};
</script>

<style lang="scss">
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
