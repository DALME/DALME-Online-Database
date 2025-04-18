<template>
  <q-item
    v-if="task.id"
    :class="task.id == selectedId && !mini ? 'selected' : ''"
    class="task-tile"
    clickable
    dense
  >
    <q-item-section @click="$emit('changeStatus')" class="cursor-pointer" avatar>
      <q-icon
        :color="task.completed ? 'light-green-8' : 'grey-8'"
        :name="task.completed ? 'mdi-checkbox-marked' : 'mdi-checkbox-blank-outline'"
        class="task-checkbox"
        size="xs"
      />
    </q-item-section>
    <q-item-section @click="$emit('viewDetail')" :no-wrap="mini" class="cursor-pointer">
      <q-item-label lines="1">
        {{ task.title }}
        <TagPill
          v-if="task.overdue && !mini"
          class="q-ml-sm"
          module="standalone"
          name="overdue"
          size="xs"
          text-colour="deep-orange-5"
          outline
        />
      </q-item-label>
      <q-item-label :lines="mini ? 1 : 2" caption>
        <template v-if="mini">
          <span v-if="task.completed" v-text="`${formatDate(task.completedDate, 'DATETIME_AT')}`" />
          <span
            v-else
            v-text="
              `${formatDate(task.creationTimestamp, 'DATETIME_AT')} | ${task.creationUser.username}`
            "
          />
        </template>
        <template v-else>
          <span v-text="`Created on ${formatDate(task.creationTimestamp, 'DATETIME_AT')} by `" />
          <DetailPopover :user-data="task.creationUser" show-avatar />
          <span
            v-if="task.completed"
            v-text="`, completed on ${formatDate(task.completedDate, 'DATETIME_AT')} by `"
          />
          <DetailPopover v-if="task.completed" :user-data="task.completedBy" show-avatar />
        </template>
        <TagPill
          v-if="task.overdue && mini"
          class="q-ml-sm"
          module="standalone"
          name="overdue"
          size="xs"
          text-colour="deep-orange-5"
          outline
        />
      </q-item-label>
    </q-item-section>
    <q-item-section v-if="mini && task.commentCount" side>
      <div class="micro-icon-comment-count">{{ task.commentCount }}</div>
    </q-item-section>
    <q-item-section v-if="!mini" side top>
      <div class="status-section">
        <q-icon
          v-if="task.commentCount"
          class="text-weight-bold q-mr-xs"
          name="mdi-message-outline"
          size="16px"
        />
        <div v-if="task.commentCount" class="text-grey-8 text-weight-bold text-detail">
          {{ task.commentCount }}
        </div>
      </div>
      <div class="status-section">
        <q-btn
          v-if="task.files.length"
          color="blue-gray-6"
          icon="mdi-paperclip"
          size="sm"
          target="_blank"
          text-color="blue-gray-6"
          dense
          flat
        />
        <q-btn
          v-if="task.url"
          @click.stop="openURL(task.url)"
          color="blue-gray-6"
          icon="mdi-link"
          size="sm"
          target="_blank"
          text-color="blue-gray-6"
          dense
          flat
        />
        <q-btn
          v-if="task.resources.length"
          color="blue-gray-6"
          icon="mdi-bookmark-outline"
          size="sm"
          target="_blank"
          text-color="blue-gray-6"
          dense
          flat
        />
      </div>
    </q-item-section>
  </q-item>

  <q-item v-else dense>
    <q-item-section avatar>
      <q-skeleton height="18px" type="rect" width="18px" />
    </q-item-section>
    <q-item-section>
      <q-skeleton height="18px" type="text" width="85%" />
      <q-skeleton height="14px" type="text" width="65%" />
    </q-item-section>
  </q-item>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, inject, toRef } from "vue";

import { DetailPopover, TagPill } from "@/components";
import { formatDate } from "@/utils";

export default defineComponent({
  name: "TaskTile",
  components: {
    DetailPopover,
    TagPill,
  },
  props: {
    data: {
      type: Object,
      default: null,
    },
    mini: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["changeStatus", "viewDetail"],
  setup(props) {
    const task = toRef(props, "data");
    const selectedId = inject("id", 0);

    return {
      formatDate,
      openURL,
      task,
      selectedId,
    };
  },
});
</script>

<style lang="scss" scoped>
.task-checkbox.mdi-checkbox-blank-outline:hover::before {
  content: "\F0C52";
}
.micro-icon-comment-count {
  font-size: 10px;
  font-weight: 800;
  display: flex;
  align-items: center;
  width: 24px;
  height: 24px;
  justify-content: center;
  margin-bottom: 5px;
}
.micro-icon-comment-count::before {
  font: normal normal normal 24px/1 "Material Design Icons";
  content: "\F017A";
  position: absolute;
  margin-top: 3px;
}
// .task-tile .q-item__label {
//   display: flex;
//   align-items: center;
// }
</style>
