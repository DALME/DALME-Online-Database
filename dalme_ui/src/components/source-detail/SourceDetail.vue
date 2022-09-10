<template>
  <div v-if="!loading">
    <div class="row">
      <div class="column full-page-height">
        <q-tabs
          v-model="tab"
          class="bg-indigo-1 text-indigo-4"
          :vertical="$q.screen.gt.xs"
          active-color="indigo-5"
          active-bg-color="indigo-2"
          indicator-color="indigo-5"
        >
          <q-tab name="info" icon="info" class="side-tab">
            <Tooltip anchor="center right" self="center left" :offset="[2, 0]">
              Info
            </Tooltip>
          </q-tab>
          <q-tab
            v-if="hasChildren"
            name="children"
            icon="account_tree"
            class="side-tab"
          >
            <Tooltip anchor="center right" self="center left" :offset="[2, 0]">
              Children
            </Tooltip>
          </q-tab>
          <q-tab
            v-if="hasPages"
            name="folios"
            icon="auto_stories"
            class="side-tab"
          >
            <Tooltip anchor="center right" self="center left" :offset="[2, 0]">
              Folios
            </Tooltip>
          </q-tab>
          <q-tab
            v-if="hasAgents || hasPlaces"
            name="entities"
            icon="person_pin_circle"
            class="side-tab"
          >
            <Tooltip anchor="center right" self="center left" :offset="[2, 0]">
              Entities (e.g. Agents, Places)
            </Tooltip>
          </q-tab>
          <q-tab name="comments" icon="forum" class="side-tab">
            <q-badge
              v-if="commentCount > 0"
              color="purple-5"
              rounded
              class="tab-badge"
            >
              {{ commentCount }}
            </q-badge>
            <Tooltip anchor="center right" self="center left" :offset="[2, 0]">
              Comments
            </Tooltip>
          </q-tab>
        </q-tabs>
      </div>
      <q-separator vertical class="tab-vertical-separator bg-indigo-2" />
      <div class="col">
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="info" class="q-pt-none">
            <SourceAttributes />
          </q-tab-panel>
          <q-tab-panel name="children" class="q-pt-none">
            <SourceChildren :children="source.children" />
          </q-tab-panel>
          <q-tab-panel name="folios" class="q-pt-none">
            <SourcePages :pages="source.pages" />
          </q-tab-panel>
          <q-tab-panel name="entities" class="q-pt-none">
            <div v-if="hasAgents">
              <SourceAgents :agents="source.agents" />
            </div>
            <div v-if="hasPlaces" class="q-mt-md">
              <SourcePlaces :places="source.places" />
            </div>
          </q-tab-panel>
          <q-tab-panel name="comments" class="q-pt-none">
            <Comments />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { useMeta } from "quasar";
import { isEmpty, isNil } from "ramda";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  inject,
  provide,
  ref,
  watch,
} from "vue";
import { useRoute } from "vue-router";
import { useNavStore } from "@/stores/navigation";

import { requests } from "@/api";
import { sourceDetailSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

import { OpaqueSpinner } from "@/components/utils";
import { Comments } from "@/components";
import SourceAttributes from "./SourceAttributes.vue";
import SourceAgents from "./SourceAgents.vue";
import SourceChildren from "./SourceChildren.vue";
import SourcePages from "./SourcePages.vue";
import SourcePlaces from "./SourcePlaces.vue";

const notNully = (value) => !isNil(value) && !isEmpty(value);

export default defineComponent({
  name: "SourceDetail",
  components: {
    Comments,
    OpaqueSpinner,
    SourceAttributes,
    SourceAgents,
    SourceChildren,
    SourcePages,
    SourcePlaces,
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const $navStore = useNavStore();
    const { loading, success, data, fetchAPI } = apiInterface();
    const source = ref({});

    const id = inject("id");

    const tab = ref("info");
    const hasAttributes = computed(() => !isNil(source.value.attributes));
    const hasAgents = computed(() => notNully(source.value.agents));
    const hasChildren = computed(() => notNully(source.value.children));
    const hasPlaces = computed(() => notNully(source.value.places));
    const hasPages = computed(() => notNully(source.value.pages));
    const commentCount = computed(() => source.value.commentCount);

    provide("model", "Source");
    provide("source", source);
    provide("hasAttributes", hasAttributes);
    provide("hasPages", hasPages);
    provide("hasChildren", hasChildren);
    provide("hasAgents", hasAgents);
    provide("hasPlaces", hasPlaces);

    useMeta(() => ({
      title: source.value ? source.value.name : `Source ${id.value}`,
    }));

    const fetchData = async () => {
      await fetchAPI(requests.sources.getSource(id.value));
      if (success.value)
        await sourceDetailSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            resource.value =
              {
                archive: "archive",
                "file unit": "archivalFile",
                record: "record",
              }[value.type.name.toLowerCase()] || "bibliography";
            source.value = value;
            $navStore.currentSubsection = value.type.name + "s";
            loading.value = false;
          });
    };

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          id.value = to;
          await fetchData();
        }
      },
      { immediate: true },
    );

    editingDetailRouteGuard();

    return {
      commentCount,
      hasAgents,
      hasAttributes,
      hasChildren,
      hasPages,
      hasPlaces,
      loading,
      source,
      tab,
    };
  },
});
</script>

<style scoped lang="scss">
.tab-vertical-separator {
  margin-left: -2px;
  z-index: 1;
  width: 2px;
}
.side-tab {
  z-index: 2;
}
.tab-badge {
  position: absolute;
  top: 3px;
  right: -1px;
}
</style>
