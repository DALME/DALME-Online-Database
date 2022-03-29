<template>
  <div class="q-ma-md full-width full-height">
    <q-card
      class="q-ma-md"
      :class="[isNil(completed) ? null : completed ? 'complete' : 'incomplete']"
    >
      <q-item>
        <q-item-section avatar>
          <q-avatar icon="assignment"> </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h5">
            <template v-if="!loading"> {{ task.title }} #{{ id }} </template>
            <template v-else>
              <q-skeleton width="30rem" />
            </template>
          </q-item-label>
          <q-item-label v-if="subheading" caption>
            {{ subheading }}
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <p v-if="!loading" class="text-body1">
          {{ task.description || "No description provided." }}
        </p>
        <q-skeleton v-else height="10rem" square />
      </q-card-section>

      <q-separator />

      <q-card-actions v-if="isAdmin">
        <q-btn @click.stop="onAction" flat>{{ action }}</q-btn>
      </q-card-actions>
      <OpaqueSpinner :showing="loading" />
    </q-card>

    <Comments />
  </div>
</template>

<script>
import { isEmpty, isNil } from "ramda";
import { useMeta } from "quasar";
import {
  computed,
  defineComponent,
  onMounted,
  provide,
  readonly,
  ref,
} from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { requests } from "@/api";
import { Comments } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { taskSchema } from "@/schemas";
import { useAPI, useEditing, useNotifier } from "@/use";

export default defineComponent({
  name: "TaskDetail",
  components: {
    Comments,
    OpaqueSpinner,
  },
  setup() {
    const $notifier = useNotifier();
    const $route = useRoute();
    const $store = useStore();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard } = useEditing();

    const model = "Task";
    const id = computed(() => $route.params.id);

    const { loading, success, data, fetchAPI } = apiInterface();
    const action = ref("");
    const completed = ref(null);
    const task = ref({});
    const attachment = ref(null);
    const subheading = ref("");
    const isAdmin = $store.getters["auth/isAdmin"];

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    useMeta(() => ({ title: `Task #${id.value}` }));

    const onAction = async () => {
      const { success, fetchAPI, status } = apiInterface();
      const action = task.value.completed ? "markUndone" : "markDone";
      await fetchAPI(requests.tasks.setTaskState(id.value, action));
      if (success.value && status.value === 201) {
        $notifier.tasks.taskStatusUpdated();
        await fetchData();
      } else {
        $notifier.tasks.taskStatusUpdatedError();
      }
    };

    const fetchData = async () => {
      await fetchAPI(requests.tasks.getTask(id.value));
      if (success.value)
        await taskSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            subheading.value =
              `${value.creationUser.fullName} created this task` +
              ` at ${value.creationTimestamp} in ${value.assignedTo}`;
            completed.value = value.completed;
            action.value = value.completed ? "reopen task" : "complete task";
            task.value = value;
            loading.value = false;
          });
    };

    editingDetailRouteGuard();
    onMounted(async () => await fetchData());

    return {
      action,
      completed,
      isAdmin,
      isEmpty,
      isNil,
      loading,
      onAction,
      subheading,
      task,
      id,
    };
  },
});
</script>

<style lang="scss" scoped>
.complete {
  border-top: 10px solid green;
}
.incomplete {
  border-top: 10px solid red;
}
</style>
