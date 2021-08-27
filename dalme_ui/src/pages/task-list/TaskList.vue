<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <TaskLists />
      </template>
    </SuspenseWithError>
    <SuspenseWithError>
      <template #default>
        <Tasks />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { groupBy } from "ramda";
import { defineComponent, provide, ref } from "vue";

import { requests } from "@/api";
import { TaskLists, Tasks } from "@/components";
import { SuspenseWithError } from "@/components/utils";
import { taskListsSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "TaskList",
  components: {
    SuspenseWithError,
    TaskLists,
    Tasks,
  },
  setup(_, context) {
    useMeta({ title: "Tasks" });
    const { success, data, fetchAPI } = useAPI(context);

    const taskLists = ref([]);

    const request = requests.tasks.taskLists();
    fetchAPI(request).then(() => {
      if (success.value)
        taskListsSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            const grouped = groupBy((tasklist) => tasklist.group, value);
            taskLists.value = grouped;
          });
    });

    provide("taskLists", taskLists);
  },
});
</script>
