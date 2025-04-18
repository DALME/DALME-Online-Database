<template>
  <q-item v-if="collection.id" class="collection-tile" clickable dense>
    <q-item-section avatar top>
      <q-icon :color="avatarIcon[1]" :name="avatarIcon[0]" size="sm" />
    </q-item-section>
    <q-item-section :no-wrap="inDrawer">
      <q-item-label lines="1">
        <div class="collection-name">{{ collection.name }}</div>
        <TagPill
          :name="collection.memberCount"
          class="q-ml-auto"
          module="standalone"
          size="xs"
          text-colour="off-blue"
          outline
        />
      </q-item-label>
      <q-item-label class="collection-description" lines="3" caption>
        {{ collection.attributes[0].value }}
      </q-item-label>
    </q-item-section>
    <q-item-section v-if="!inDrawer" side top>
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
</template>

<script>
import { openURL } from "quasar";
import { computed, defineComponent } from "vue";

import { TagPill } from "@/components";

export default defineComponent({
  name: "CollectionTile",
  components: {
    TagPill,
  },
  props: {
    collection: {
      type: Object,
      default: null,
    },
    inDrawer: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["changeStatus", "goToTask"],
  setup(props) {
    const avatarIcon = computed(() => {
      if (props.collection.isPublished) {
        return ["mdi-folder-eye-outline", "light-green-8"];
      } else if (props.collection.useAsWorkset) {
        return ["mdi-folder-wrench-outline", "indigo-4"];
      } else if (props.collection.isPrivate) {
        return ["mdi-folder-lock-outline", "deep-orange-5"];
      } else {
        return ["mdi-folder-outline", "off-blue"];
      }
    });

    return {
      openURL,
      avatarIcon,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-item.collection-tile .q-item__label {
  display: flex;
  text-wrap: auto;
  list-style: none;
}
.custom-drawer.app-drawer .collection-name {
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}
.collection-description {
  line-height: 1.3 !important;
}
</style>
