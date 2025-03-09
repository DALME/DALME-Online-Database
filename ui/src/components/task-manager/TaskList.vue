<template>
  <q-expansion-item
    v-if="inUserDrawer"
    :label="label"
    default-opened
    header-class="drawer_expansion_header"
    expand-icon="mdi-plus-box-outline"
    expanded-icon="mdi-minus-box-outline"
  >
    <template v-if="!loading">
      <template v-if="taskData.length > 0">
        <TaskTile
          v-for="(task, idx) in taskData"
          :key="idx"
          :data="task"
          mini
          @change-status="$emit('changeStatus', task)"
          @view-detail="$emit('viewDetail', task)"
        />
      </template>
      <q-item v-else class="q-px-sm q-py-md">
        <q-item-section>
          <q-item-label class="text-caption">{{ noDataMessage }}</q-item-label>
        </q-item-section>
      </q-item>
      <div class="task-list-actions" v-if="addNewButton || showMoreButton">
        <q-btn
          v-if="showMoreButton"
          flat
          no-caps
          label="Show more..."
          class="task-action"
          @click="$emit('showMore')"
        />
        <q-btn
          v-if="addNewButton"
          flat
          no-caps
          label="Add new"
          icon="mdi-checkbox-marked-circle-plus-outline"
          class="task-action"
          @click="$emit('showMore')"
        />
      </div>
    </template>
    <template v-if="loading">
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton type="rect" height="18px" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton type="text" height="18px" width="85%" />
          <q-skeleton type="text" height="14px" width="65%" />
        </q-item-section>
      </q-item>
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton type="rect" height="18px" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton type="text" height="18px" width="85%" />
          <q-skeleton type="text" height="14px" width="65%" />
        </q-item-section>
      </q-item>
    </template>
  </q-expansion-item>
  <q-list v-else class="drawer-menu-list scroll-area">
    <template v-if="!loading">
      <template v-if="taskData.length > 0">
        <TaskTile
          v-for="(task, idx) in taskData"
          ref="tileRefs"
          :key="idx"
          :data="task"
          @change-status="$emit('changeStatus', task)"
          @view-detail="$emit('viewDetail', task)"
        />
        <q-btn
          v-if="showMoreButton"
          flat
          no-caps
          label="Show more..."
          class="task-action"
          @click="$emit('showMore')"
        />
      </template>
      <q-item v-else class="q-px-sm q-py-md">
        <q-item-section>
          <q-item-label class="text-center text-blue-grey-6" style="line-height: 1.4 !important">
            {{ noDataMessage }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </template>
    <template v-if="loading">
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton type="rect" height="18px" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton type="text" height="18px" width="85%" />
          <q-skeleton type="text" height="14px" width="65%" />
        </q-item-section>
      </q-item>
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton type="rect" height="18px" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton type="text" height="18px" width="85%" />
          <q-skeleton type="text" height="14px" width="65%" />
        </q-item-section>
      </q-item>
    </template>
  </q-list>
</template>

<script>
import { defineComponent, inject, onMounted, ref, toRef } from "vue";
import { filter as rFilter } from "ramda";
import TaskTile from "./TaskTile.vue";

export default defineComponent({
  name: "TaskList",
  props: {
    data: {
      type: Array,
      default: null,
    },
    loading: {
      type: Boolean,
    },
    label: {
      type: String,
      default: "Tasks",
    },
    inUserDrawer: {
      type: Boolean,
      default: false,
    },
    moreButton: {
      type: Boolean,
      default: false,
    },
    addNewButton: {
      type: Boolean,
      default: false,
    },
    noDataMessage: {
      type: String,
      default: "No tasks available.",
    },
    scrollOff: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    TaskTile,
  },
  emits: ["showMore", "changeStatus", "viewDetail"],
  setup(props, _) {
    const taskData = toRef(props, "data");
    const showMoreButton = toRef(props, "moreButton");
    const tileRefs = ref([]);
    const selectedId = inject("id", 0);

    onMounted(async () => {
      if (!props.inUserDrawer && !props.scrollOff && selectedId.value != 0) {
        const target = rFilter((x) => x.task.id == selectedId.value, tileRefs.value);
        target[0].$el.scrollIntoView();
      }
    });

    return {
      showMoreButton,
      taskData,
      tileRefs,
    };
  },
});
</script>
