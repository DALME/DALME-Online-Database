<template>
  <Page>
    <TaskLists @on-reload="handleReload" />
    <Tasks />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { groupBy } from "ramda";
import { defineComponent, onMounted, provide, ref } from "vue";

import { requests } from "@/api";
import { Page, TaskLists, Tasks } from "@/components";
import { taskListsSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "TaskList",
  components: {
    Page,
    TaskLists,
    Tasks,
  },
  setup() {
    useMeta({ title: "Tasks" });
    const { apiInterface } = useAPI();
    const { postSubmitRefreshWatcher } = useEditing();

    const { success, data, fetchAPI } = apiInterface();
    const taskLists = ref([]);
    provide("taskLists", taskLists);

    const fetchData = async () => {
      const request = requests.tasks.getTaskLists();
      fetchAPI(request).then(() => {
        if (success.value)
          taskListsSchema
            .validate(data.value, { stripUnknown: true })
            .then((value) => {
              const grouped = groupBy((tasklist) => tasklist.group.name, value);
              taskLists.value = grouped;
            });
      });
    };

    postSubmitRefreshWatcher(fetchData);
    onMounted(async () => await fetchData());

    return {
      handleReload: fetchData,
    };
  },
});
</script>
