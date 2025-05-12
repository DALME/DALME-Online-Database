<template>
  <div v-if="!loading && !isEmpty(task)" class="full-width full-height">
    <div class="info-area row">
      <div class="col-grow">
        <div class="row items-center text-h5">
          {{ task.title }}
        </div>
        <div class="row detail-row-subheading text-grey-8">
          <q-chip
            :color="task.completed ? 'red-6' : 'green-7'"
            :icon="task.completed ? 'o_check_circle' : 'o_error_outline'"
            :label="task.completed ? 'Completed' : 'Incomplete'"
            class="q-ml-none q-mr-xs"
            size="sm"
            text-color="white"
          />
          <DetailPopover :show-avatar="false" :user-data="task.creationUser" />
          created this task on {{ formatDate(task.creationTimestamp, "DATETIME_AT") }}
        </div>
      </div>
      <div v-if="isAdmin" class="col-auto">
        <q-btn
          @click.stop="onAction"
          :class="`action-button bg-${buttonColours.colour}`"
          :color="buttonColours.colour"
          :label="capitalize(action)"
          :text-color="buttonColours.text"
          dense
          no-caps
          outline
        />
      </div>
    </div>
    <q-separator class="q-mb-lg" />
    <div class="row">
      <div class="col-9 q-pr-md">
        <q-card class="q-mb-md" flat>
          <q-card-section
            :class="
              task.commentCount > 0
                ? 'q-pt-none q-pr-none'
                : 'q-pt-none q-pr-none comments-container'
            "
          >
            <div class="comment-thread q-mt-none q-pb-lg">
              <q-item class="q-pb-sm q-pt-none q-px-none">
                <q-item-section avatar top>
                  <q-avatar v-if="task.creationUser.avatar" size="40px">
                    <q-img :src="task.creationUser.avatar" fit="cover" ratio="1" />
                  </q-avatar>
                  <q-avatar
                    v-else
                    color="grey-4"
                    icon="account_circle"
                    size="40px"
                    text-color="grey-6"
                  />
                </q-item-section>
                <q-item-section>
                  <q-card class="box-left-arrow" bordered flat>
                    <q-card-section class="bg-grey-2 comment-head">
                      <DetailPopover :show-avatar="false" :user-data="task.creationUser" />
                      commented on {{ formatDate(task.creationTimestamp, "DATETIME_AT") }}
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="text-body2">
                      <MarkdownEditor v-if="task.description" :text="task.description" />
                      <span v-else>No description provided.</span>
                    </q-card-section>
                  </q-card>
                </q-item-section>
              </q-item>
            </div>
            <CommentBox>
              <template v-if="task.completed" #comment-stream-end>
                <div class="comment-thread row items-center q-mt-none q-pb-lg">
                  <div class="closing-dot bg-deep-purple-6">
                    <q-icon color="white" name="o_check_circle" size="20px" />
                  </div>
                  <div class="closing-dot-label">
                    this task was completed {{ formatDate(task.completedDate, "DATETIME_AT") }}
                  </div>
                </div>
              </template>
            </CommentBox>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-3 q-pl-md">
        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">Assignees</div>
        <div class="q-mb-sm text-13">
          <span>No one assigned</span>
        </div>
        <q-separator class="q-my-md" />

        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">Attachments</div>
        <div class="q-mb-sm text-13">
          <AttachmentWidget v-if="attachment" />
          <span v-else>None yet</span>
        </div>
        <q-separator class="q-my-md" />

        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">Links</div>
        <div class="q-mb-sm text-13">
          <span>None yet</span>
        </div>
      </div>
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { format, useMeta } from "quasar";
import { isEmpty } from "ramda";
import { computed, defineComponent, onMounted, provide, readonly, ref } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import {
  AttachmentWidget,
  CommentBox,
  DetailPopover,
  MarkdownEditor,
  OpaqueSpinner,
} from "@/components";
import { taskSchema } from "@/schemas";
import { useAPI, useEventHandling, useStores } from "@/use";
import { formatDate } from "@/utils";

export default defineComponent({
  name: "TaskDetail",
  components: {
    AttachmentWidget,
    CommentBox,
    DetailPopover,
    MarkdownEditor,
    OpaqueSpinner,
  },
  setup() {
    const { notifier } = useEventHandling();
    const $route = useRoute();
    const { auth, ui } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { capitalize } = format;
    const model = "Task";
    const action = ref("");
    const attachment = ref(null);
    const task = ref({});
    const id = computed(() => $route.params.id);
    const buttonColours = computed(() =>
      action.value === "reopen task"
        ? { colour: "green-1", text: "green-7" }
        : { colour: "deep-purple-1", text: "deep-purple-6" },
    );

    useMeta(() => ({ title: `Task #${id.value}` }));
    ui.breadcrumbTail.push(`#${id.value}`);

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    const onAction = async () => {
      const { success, fetchAPI, status } = apiInterface();
      const action = task.value.completed ? "markUndone" : "markDone";
      await fetchAPI(requests.tasks.setState(id.value, action));
      if (success.value && status.value === 201) {
        notifier.tasks.taskStatusUpdated();
        await fetchData();
      } else {
        notifier.tasks.taskStatusUpdatedError();
      }
    };

    const fetchData = async () => {
      await fetchAPI(requests.tasks.get(id.value));
      if (success.value)
        await taskSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          action.value = value.completed ? "reopen task" : "complete task";
          task.value = value;
          attachment.value = value.file;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());
    onBeforeRouteLeave(() => {
      ui.resetBreadcrumbTail();
    });

    return {
      action,
      attachment,
      buttonColours,
      capitalize,
      formatDate,
      isAdmin: auth.user.isSuperuser,
      isEmpty,
      loading,
      onAction,
      task,
    };
  },
});
</script>

<style lang="scss" scoped>
.action-button {
  padding: 0px 10px 0px 10px;
  font-weight: 600;
  font-size: 14px;
}
</style>
