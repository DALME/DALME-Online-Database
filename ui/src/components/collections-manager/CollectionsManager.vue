<template>
  <q-item class="collections-item" header-class="drawer_expansion_header">
    <q-item class="drawer_expansion_header">
      <q-item-section class="justify-center">
        <q-item-label>{{ label }}</q-item-label>
      </q-item-section>
    </q-item>
    <q-scroll-area
      :style="`height: 100%; width: ${width}px; min-width: ${width}px`"
      class="scroll-area"
      dark
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
            @click="limit = limit + 5"
            class="drawer-show-more"
            label="Show more..."
            flat
            no-caps
          />
        </div>
      </template>
      <template v-if="loading">
        <template v-for="idx in limit" :key="idx">
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
      </template>
    </q-scroll-area>
  </q-item>
</template>

<script>
import { computed, defineComponent, onMounted, ref, watch } from "vue";

import { requests } from "@/api";
import { collectionsSchema } from "@/schemas";
import { useAPI, useStores } from "@/use";

import CollectionTile from "./CollectionTile.vue";

export default defineComponent({
  name: "CollectionsManager",
  components: {
    CollectionTile,
  },
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
