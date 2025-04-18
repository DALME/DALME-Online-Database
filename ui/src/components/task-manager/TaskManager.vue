<template>
  <template v-if="taskStore.ready">
    <TaskList
      @change-status="taskStore.onChangeStatus"
      @show-more="taskStore.onShowMore('created')"
      @view-detail="onViewDetail"
      :data="taskStore.created"
      :loading="taskStore.loading"
      :more-button="taskStore.moreCreated"
      :no-data-message="createdNoData"
      label="Your tasks"
      add-new-button
      in-user-drawer
    />
    <TaskList
      @change-status="taskStore.onChangeStatus"
      @show-more="taskStore.onShowMore('assigned')"
      @view-detail="onViewDetail"
      :data="taskStore.assigned"
      :loading="taskStore.loading"
      :more-button="taskStore.moreAssigned"
      :no-data-message="assignedNoData"
      label="Tasks assigned to you"
      in-user-drawer
    />
    <TaskList
      @change-status="taskStore.onChangeStatus"
      @show-more="taskStore.onShowMore('completed')"
      @view-detail="onViewDetail"
      :data="taskStore.completed"
      :loading="taskStore.loading"
      :more-button="taskStore.moreCompleted"
      label="Tasks you completed"
      no-data-message="You have not completed any tasks yet."
      in-user-drawer
    />
  </template>
</template>

<script>
import { computed, defineComponent } from "vue";

import { useStores } from "@/use";

import TaskList from "./TaskList.vue";

export default defineComponent({
  name: "TaskManager",
  components: {
    TaskList,
  },
  setup() {
    const { taskStore } = useStores();

    const onViewDetail = (task) => {
      taskStore.setViewer(task);
      taskStore.showTaskModal();
    };

    const createdNoData = computed(() => {
      if (taskStore.meta.user > 0) {
        return "There are no pending tasks.";
      } else {
        return "You have not created any tasks yet.";
      }
    });

    const assignedNoData = computed(() => {
      if (taskStore.meta.assigned > 0) {
        return "There are no pending tasks assigned to you.";
      } else {
        return "You have not been assigned any tasks yet.";
      }
    });

    return {
      taskStore,
      onViewDetail,
      createdNoData,
      assignedNoData,
    };
  },
});
</script>
