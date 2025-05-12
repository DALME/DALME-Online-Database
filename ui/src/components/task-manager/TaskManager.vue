<template>
  <TaskList
    @change-status="Tasks.onChangeStatus"
    @show-more="Tasks.onShowMore('created')"
    @view-detail="onViewDetail"
    :data="Tasks.created"
    :loading="loading"
    :more-button="Tasks.moreCreated"
    :no-data-message="createdNoData"
    label="Your tasks"
    add-new-button
    in-user-drawer
  />
  <TaskList
    @change-status="Tasks.onChangeStatus"
    @show-more="Tasks.onShowMore('assigned')"
    @view-detail="onViewDetail"
    :data="Tasks.assigned"
    :loading="loading"
    :more-button="Tasks.moreAssigned"
    :no-data-message="assignedNoData"
    label="Tasks assigned to you"
    in-user-drawer
  />
  <TaskList
    @change-status="Tasks.onChangeStatus"
    @show-more="Tasks.onShowMore('completed')"
    @view-detail="onViewDetail"
    :data="Tasks.completed"
    :loading="loading"
    :more-button="Tasks.moreCompleted"
    label="Tasks you completed"
    no-data-message="You have not completed any tasks yet."
    in-user-drawer
  />
</template>

<script>
import { computed, defineComponent, onBeforeMount, ref } from "vue";

import { TaskLists, Tasks } from "@/models";
import { useStores } from "@/use";

import TaskList from "./TaskList.vue";

export default defineComponent({
  name: "TaskManager",
  components: {
    TaskList,
  },
  setup() {
    const { auth } = useStores();
    const loading = ref(false);

    const onViewDetail = (task) => {
      Tasks.setCurrent(task);
      Tasks.showModal();
    };

    const createdNoData = computed(() => {
      if (Tasks.totalCounts.user > 0) {
        return "There are no pending tasks.";
      } else {
        return "You have not created any tasks yet.";
      }
    });

    const assignedNoData = computed(() => {
      if (Tasks.totalCounts.assigned > 0) {
        return "There are no pending tasks assigned to you.";
      } else {
        return "You have not been assigned any tasks yet.";
      }
    });

    onBeforeMount(() => {
      loading.value = true;
      Promise.all([TaskLists.init(auth.user.id), Tasks.init(auth.user.id)]).then(() => {
        loading.value = false;
      });
    });

    return {
      onViewDetail,
      createdNoData,
      assignedNoData,
      loading,
      Tasks,
    };
  },
});
</script>
