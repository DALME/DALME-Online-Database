<template>
  <template v-if="tm.tasksReady">
    <TaskList
      add-new-button
      :data="tm.created"
      label="Your tasks"
      in-user-drawer
      :no-data-message="createdNoData"
      :more-button="tm.moreCreated"
      @show-more="tm.onShowMore('created')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="tm.assigned"
      label="Tasks assigned to you"
      in-user-drawer
      :no-data-message="assignedNoData"
      :more-button="tm.moreAssigned"
      @show-more="tm.onShowMore('assigned')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="tm.completed"
      label="Tasks you completed"
      in-user-drawer
      no-data-message="You have not completed any tasks yet."
      :more-button="tm.moreCompleted"
      @show-more="tm.onShowMore('completed')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
  </template>
</template>

<script>
import { computed, defineComponent, onMounted } from "vue";
import { useTasks } from "@/stores/tasks";
import TaskList from "./TaskList.vue";

export default defineComponent({
  name: "TaskManager",
  components: {
    TaskList,
  },
  setup() {
    const tm = useTasks();

    const onViewDetail = (task) => {
      tm.setViewing(task);
      tm.showTaskModal();
    };

    const createdNoData = computed(() => {
      if (tm.tasksMeta.user > 0) {
        return "There are no pending tasks.";
      } else {
        return "You have not created any tasks yet.";
      }
    });

    const assignedNoData = computed(() => {
      if (tm.tasksMeta.assigned > 0) {
        return "There are no pending tasks assigned to you.";
      } else {
        return "You have not been assigned any tasks yet.";
      }
    });

    onMounted(async () => await tm.init("tasks"));

    return {
      tm,
      onViewDetail,
      createdNoData,
      assignedNoData,
    };
  },
});
</script>
