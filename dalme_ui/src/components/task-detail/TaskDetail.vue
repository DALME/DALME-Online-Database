<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-item :class="colour">
        <q-item-section avatar>
          <q-avatar icon="assignment"> </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h5">
            {{ task.title }}
            <span>#{{ id }}</span>
          </q-item-label>
          <q-item-label caption>{{ subheading }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <p class="text-body1">{{ task.description }}</p>
      </q-card-section>

      <q-separator />

      <q-card-actions v-if="isAdmin">
        <q-btn @click="onAction" flat>{{ action }}</q-btn>
      </q-card-actions>
    </q-card>

    <Comments />
  </div>
</template>

<script>
import { defineComponent, provide, readonly, ref } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { requests } from "@/api";
import { Comments } from "@/components";
import { taskSchema } from "@/schemas";
import { useAPI, useNotifier } from "@/use";

export default defineComponent({
  name: "TaskDetail",
  components: {
    Comments,
  },
  async setup(_, context) {
    const $route = useRoute();
    const $store = useStore();
    const { success, data, fetchAPI } = useAPI(context);
    const {
      success: actionSuccess,
      fetchAPI: actionFetchAPI,
      status: actionStatus,
    } = useAPI(context);
    const $notifier = useNotifier();

    const action = ref("");
    const colour = ref("");
    const task = ref(null);
    const attachment = ref(null);
    const id = ref($route.params.id);
    const isAdmin = $store.getters["auth/isAdmin"];

    let subheading = "";
    const model = "Task";

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    const onAction = async () => {
      const action = task.value.completed ? "markUndone" : "markDone";
      await actionFetchAPI(requests.tasks.setTaskState(id.value, action));
      if (actionSuccess.value && actionStatus.value === 201) {
        await fetchData();
        $notifier.tasks.taskStatusUpdated();
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
            subheading =
              `${value.owner} created this task` +
              ` at ${value.creationTimestamp} in ${value.assignedTo}`;
            action.value = value.completed ? "reopen task" : "complete task";
            colour.value = value.completed
              ? "bg-green-5 text-grey-1"
              : "bg-red-12 text-grey-1";
            task.value = value;
          });
    };

    await fetchData();

    return {
      action,
      colour,
      isAdmin,
      onAction,
      subheading,
      task,
      id,
    };
  },
});
</script>
