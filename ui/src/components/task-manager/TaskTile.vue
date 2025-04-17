<template>
  <q-item
    dense
    clickable
    v-if="task.id"
    class="task-tile"
    :class="task.id == selectedId && !mini ? 'selected' : ''"
  >
    <q-item-section avatar @click="$emit('changeStatus')" class="cursor-pointer">
      <q-icon
        :name="task.completed ? 'mdi-checkbox-marked' : 'mdi-checkbox-blank-outline'"
        :color="task.completed ? 'light-green-8' : 'grey-8'"
        size="xs"
        class="task-checkbox"
      />
    </q-item-section>
    <q-item-section :no-wrap="mini" @click="$emit('viewDetail')" class="cursor-pointer">
      <q-item-label lines="1">
        {{ task.title }}
        <TagPill
          v-if="task.overdue && !mini"
          outline
          name="overdue"
          text-colour="deep-orange-5"
          size="xs"
          module="standalone"
          class="q-ml-sm"
        />
      </q-item-label>
      <q-item-label caption :lines="mini ? 1 : 2">
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
          <DetailPopover show-avatar :user-data="task.creationUser" />
          <span
            v-if="task.completed"
            v-text="`, completed on ${formatDate(task.completedDate, 'DATETIME_AT')} by `"
          />
          <DetailPopover v-if="task.completed" show-avatar :user-data="task.completedBy" />
        </template>
        <TagPill
          v-if="task.overdue && mini"
          outline
          name="overdue"
          text-colour="deep-orange-5"
          size="xs"
          module="standalone"
          class="q-ml-sm"
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
          name="mdi-message-outline"
          size="16px"
          class="text-weight-bold q-mr-xs"
        />
        <div v-if="task.commentCount" class="text-grey-8 text-weight-bold text-detail">
          {{ task.commentCount }}
        </div>
      </div>
      <div class="status-section">
        <q-btn
          v-if="task.files.length"
          flat
          dense
          target="_blank"
          color="blue-gray-6"
          size="sm"
          icon="mdi-paperclip"
          text-color="blue-gray-6"
        />
        <q-btn
          v-if="task.url"
          flat
          dense
          @click.stop="openURL(task.url)"
          target="_blank"
          color="blue-gray-6"
          size="sm"
          icon="mdi-link"
          text-color="blue-gray-6"
        />
        <q-btn
          v-if="task.resources.length"
          flat
          dense
          target="_blank"
          color="blue-gray-6"
          size="sm"
          icon="mdi-bookmark-outline"
          text-color="blue-gray-6"
        />
      </div>
    </q-item-section>
  </q-item>

  <q-item dense v-else>
    <q-item-section avatar>
      <q-skeleton type="rect" height="18px" width="18px" />
    </q-item-section>
    <q-item-section>
      <q-skeleton type="text" height="18px" width="85%" />
      <q-skeleton type="text" height="14px" width="65%" />
    </q-item-section>
  </q-item>
</template>

<script>
import { openURL } from "quasar";
import { defineComponent, inject, toRef } from "vue";
import { formatDate } from "@/utils";
import { DetailPopover, TagPill } from "@/components";

export default defineComponent({
  name: "TaskTile",
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
  components: {
    DetailPopover,
    TagPill,
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

<style lang="scss">
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
