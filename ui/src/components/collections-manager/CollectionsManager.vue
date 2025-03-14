<template>
  <q-item header-class="drawer_expansion_header" class="collections-item">
    <q-item class="drawer_expansion_header">
      <q-item-section class="justify-center">
        <q-item-label>{{ label }}</q-item-label>
      </q-item-section>
    </q-item>
    <q-scroll-area
      dark
      :style="`height: 100%; width: ${width}px; min-width: ${width}px`"
      class="scroll-area"
    >
      <template v-if="!loading">
        <CollectionTile
          v-for="(collection, idx) in collections"
          :key="idx"
          :collection="collection"
          :in-drawer="inDrawer"
        />
        <div class="flex task-list-actions">
          <q-btn
            v-if="totalCount > currentCount"
            flat
            no-caps
            label="Show more..."
            class="drawer-show-more"
            @click="limit = limit + 5"
          />
        </div>
      </template>
      <template v-if="loading">
        <template v-for="idx in limit" :key="idx">
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
      </template>
    </q-scroll-area>
  </q-item>
</template>

<script>
import { computed, defineComponent, ref, onMounted, watch } from "vue";
import { requests } from "@/api";
import { useStores, useAPI } from "@/use";
import { collectionsSchema } from "@/schemas";
import CollectionTile from "./CollectionTile.vue";

export default defineComponent({
  name: "CollectionsManager",
  props: {
    userCollections: {
      type: Boolean,
      default: false,
    },
    teamCollections: {
      type: Boolean,
      default: false,
    },
    inDrawer: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: "Collections",
    },
    scrollHeight: Number,
    width: String,
  },
  components: {
    CollectionTile,
  },
  setup(props, context) {
    const { auth } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const collections = ref([]);
    const limit = ref(props.inDrawer ? 15 : null);
    const totalCount = ref(0);
    const currentCount = ref(0);

    const request = computed(() => {
      if (props.userCollections) {
        return requests.collections.getUserCollections(auth.user.userId, limit.value);
      } else if (props.teamCollections) {
        return requests.collections.getTeamCollections(auth.user.userId, limit.value);
      } else {
        return requests.collections.getCollections();
      }
    });

    const fetchData = async () => {
      if (auth.authorized) {
        await fetchAPI(request.value);
        if (success.value)
          await collectionsSchema
            .validate(data.value.data, { stripUnknown: false })
            .then((value) => {
              collections.value = value;
              totalCount.value = data.value.count;
              currentCount.value = data.value.filtered;
              loading.value = false;
            });
      }
    };

    onMounted(async () => await fetchData());

    watch(
      () => limit.value,
      () => fetchData(),
    );

    return {
      context,
      loading,
      collections,
      limit,
      totalCount,
      currentCount,
    };
  },
});
</script>

<style lang="scss" scoped>
.collections-item {
  flex-direction: column;
  flex-grow: 1;
  padding: 0;
  margin: 0;
  border-top: 1px solid var(--dark-border-base-colour);
  border-radius: 0;
}
</style>
