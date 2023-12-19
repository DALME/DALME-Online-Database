<template>
  <q-expansion-item
    :label="label"
    default-opened
    header-class="drawer_expansion_header"
    expand-icon="mdi-plus-box-outline"
    expanded-icon="mdi-minus-box-outline"
  >
    <template v-if="!loading">
      <CollectionTile
        v-for="(collection, idx) in collections"
        :key="idx"
        :collection="collection"
        :in-drawer="inDrawer"
      />
      <div class="flex">
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
  </q-expansion-item>
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
    userCollectionsOnly: {
      type: Boolean,
      default: false,
    },
    teamCollectionsOnly: {
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
      if (props.userCollectionsOnly) {
        return requests.collections.getUserCollections(auth.user.userId, limit.value);
      } else if (props.teamCollectionsOnly) {
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
