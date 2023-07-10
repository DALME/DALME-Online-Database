<template>
  <template v-if="tm.tasksReady">
    <TaskList
      add-new-button
      :data="tm.created"
      label="Your tasks"
      in-user-drawer
      :more-button="tm.moreCreated"
      @show-more="tm.onShowMore('created')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="tm.assigned"
      label="Tasks assigned to you"
      in-user-drawer
      :more-button="tm.moreAssigned"
      @show-more="tm.onShowMore('assigned')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
    <TaskList
      :data="tm.completed"
      label="Tasks you completed"
      in-user-drawer
      :more-button="tm.moreCompleted"
      @show-more="tm.onShowMore('completed')"
      @change-status="tm.onChangeStatus"
      @view-detail="onViewDetail"
    />
  </template>
</template>

<script>
import { useQuasar } from "quasar";
import { defineComponent, onMounted } from "vue";
import { useTasks } from "@/stores/tasks";
import TaskList from "./TaskList.vue";
import TaskViewer from "./TaskViewer.vue";

export default defineComponent({
  name: "TaskManager",
  components: {
    TaskList,
  },
  setup() {
    const $q = useQuasar();
    const tm = useTasks();

    const onViewDetail = (task) => {
      tm.setViewing(task);
      $q.dialog({ component: TaskViewer });
    };

    onMounted(async () => await tm.init("tasks"));

    return {
      tm,
      onViewDetail,
    };
  },
});
</script>
