<template>
  <Page>
    <Tasks @on-reload-task-lists="handleReload" />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { groupBy } from "ramda";
import { defineComponent, onMounted, provide, ref } from "vue";
import { requests } from "@/api";
import { Page, Tasks } from "@/components";
import { taskListsSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "TaskList",
  components: {
    Page,
    Tasks,
  },
  setup() {
    useMeta({ title: "Tasks" });
    const { apiInterface } = useAPI();
    const { postSubmitRefreshWatcher } = useEditing();
    const { success, data, fetchAPI } = apiInterface();
    const taskLists = ref([]);

    const fetchData = async () => {
      const request = requests.tasks.getTaskLists();
      fetchAPI(request).then(() => {
        if (success.value)
          taskListsSchema
            .validate(data.value.data, { stripUnknown: true })
            .then((value) => {
              const grouped = groupBy((tasklist) => tasklist.group.name, value);
              taskLists.value = grouped;
            });
      });
    };

    provide("taskLists", taskLists);
    postSubmitRefreshWatcher(fetchData);
    onMounted(async () => await fetchData());

    return {
      handleReload: fetchData,
    };
  },
});
</script>
