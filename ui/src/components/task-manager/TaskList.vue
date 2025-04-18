<template>
  <q-expansion-item
    v-if="inUserDrawer"
    :label="label"
    expand-icon="mdi-plus-box-outline"
    expanded-icon="mdi-minus-box-outline"
    header-class="drawer_expansion_header"
    default-opened
  >
    <template v-if="!loading">
      <template v-if="taskData.length > 0">
        <TaskTile
          v-for="(task, idx) in taskData"
          :key="idx"
          @change-status="$emit('changeStatus', task)"
          @view-detail="$emit('viewDetail', task)"
          :data="task"
          mini
        />
      </template>
      <q-item v-else class="q-px-sm q-py-md">
        <q-item-section>
          <q-item-label class="text-caption">{{ noDataMessage }}</q-item-label>
        </q-item-section>
      </q-item>
      <div v-if="addNewButton || showMoreButton" class="task-list-actions">
        <q-btn
          v-if="showMoreButton"
          @click="$emit('showMore')"
          class="task-action"
          label="Show more..."
          flat
          no-caps
        />
        <q-btn
          v-if="addNewButton"
          @click="$emit('showMore')"
          class="task-action"
          icon="mdi-checkbox-marked-circle-plus-outline"
          label="Add new"
          flat
          no-caps
        />
      </div>
    </template>
    <template v-if="loading">
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton height="18px" type="rect" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton height="18px" type="text" width="85%" />
          <q-skeleton height="14px" type="text" width="65%" />
        </q-item-section>
      </q-item>
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton height="18px" type="rect" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton height="18px" type="text" width="85%" />
          <q-skeleton height="14px" type="text" width="65%" />
        </q-item-section>
      </q-item>
    </template>
  </q-expansion-item>
  <q-list v-else class="drawer-menu-list scroll-area">
    <template v-if="!loading">
      <template v-if="taskData.length > 0">
        <TaskTile
          v-for="(task, idx) in taskData"
          :key="idx"
          ref="tileRefs"
          @change-status="$emit('changeStatus', task)"
          @view-detail="$emit('viewDetail', task)"
          :data="task"
        />
        <q-btn
          v-if="showMoreButton"
          @click="$emit('showMore')"
          class="task-action"
          label="Show more..."
          flat
          no-caps
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
          <q-skeleton height="18px" type="rect" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton height="18px" type="text" width="85%" />
          <q-skeleton height="14px" type="text" width="65%" />
        </q-item-section>
      </q-item>
      <q-item dense>
        <q-item-section avatar>
          <q-skeleton height="18px" type="rect" width="18px" />
        </q-item-section>
        <q-item-section>
          <q-skeleton height="18px" type="text" width="85%" />
          <q-skeleton height="14px" type="text" width="65%" />
        </q-item-section>
      </q-item>
    </template>
  </q-list>
</template>

<script>
import { filter as rFilter } from "ramda";
import { defineComponent, inject, onMounted, ref, toRef } from "vue";

import TaskTile from "./TaskTile.vue";

export default defineComponent({
  name: "TaskList",
  components: {
    TaskTile,
  },
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
