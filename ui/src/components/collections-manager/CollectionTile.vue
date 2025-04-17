<template>
  <q-item dense clickable v-if="collection.id" class="collection-tile">
    <q-item-section avatar top>
      <q-icon :name="avatarIcon[0]" :color="avatarIcon[1]" size="sm" />
    </q-item-section>
    <q-item-section :no-wrap="inDrawer">
      <q-item-label lines="1">
        <div class="collection-name">{{ collection.name }}</div>
        <TagPill
          :name="collection.memberCount"
          outline
          text-colour="off-blue"
          size="xs"
          module="standalone"
          class="q-ml-auto"
        />
      </q-item-label>
      <q-item-label caption class="collection-description" lines="3">
        {{ collection.attributes[0].value }}
      </q-item-label>
    </q-item-section>
    <q-item-section v-if="!inDrawer" side top>
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
</template>

<script>
import { openURL } from "quasar";
import { computed, defineComponent } from "vue";
import { TagPill } from "@/components";

export default defineComponent({
  name: "CollectionTile",
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
  components: {
    TagPill,
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
