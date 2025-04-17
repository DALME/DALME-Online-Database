<template>
  <template v-if="taskStore.ready">
    <TaskList
      add-new-button
      :data="taskStore.created"
      :loading="taskStore.loading"
      label="Your tasks"
      in-user-drawer
      :no-data-message="createdNoData"
      :more-button="taskStore.moreCreated"
      @show-more="taskStore.onShowMore('created')"
      @change-status="taskStore.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="taskStore.assigned"
      :loading="taskStore.loading"
      label="Tasks assigned to you"
      in-user-drawer
      :no-data-message="assignedNoData"
      :more-button="taskStore.moreAssigned"
      @show-more="taskStore.onShowMore('assigned')"
      @change-status="taskStore.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="taskStore.completed"
      :loading="taskStore.loading"
      label="Tasks you completed"
      in-user-drawer
      no-data-message="You have not completed any tasks yet."
      :more-button="taskStore.moreCompleted"
      @show-more="taskStore.onShowMore('completed')"
      @change-status="taskStore.onChangeStatus"
      @view-detail="onViewDetail"
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
