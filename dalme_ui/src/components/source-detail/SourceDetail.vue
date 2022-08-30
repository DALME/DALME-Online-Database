<template>
  <div v-if="!loading">
    <q-splitter
      :horizontal="$q.screen.lt.sm"
      v-model="splitterModel"
      class="full-page-height"
    >
      <template v-slot:before>
        <q-tabs
          v-model="tab"
          class="text-light-blue-9"
          :vertical="$q.screen.gt.xs"
          active-bg-color="light-blue-1"
          indicator-color="light-blue-9"
          no-caps
        >
          <q-tab name="attributes" icon="info" label="Attributes" />
          <q-tab
            v-if="hasChildren"
            name="children"
            icon="account_tree"
            label="Children"
          />
          <q-tab
            v-if="hasPages"
            name="folios"
            icon="auto_stories"
            label="Folios"
          />
          <q-tab
            v-if="hasAgents || hasPlaces"
            name="agentsAndPlaces"
            icon="person_pin_circle"
            label="Agents/Places"
          />
          <q-tab name="comments" icon="forum" label="Discussion" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="attributes"><SourceAttributes /></q-tab-panel>
          <q-tab-panel name="children"><SourceChildren /></q-tab-panel>
          <q-tab-panel name="folios"><SourcePages /></q-tab-panel>
          <q-tab-panel name="agentsAndPlaces">
            <q-card v-if="hasAgents" class="q-mt-md">
              <SourceAgents />
            </q-card>
            <q-card v-if="hasPlaces" class="q-mt-md">
              <SourcePlaces />
            </q-card>
          </q-tab-panel>
          <q-tab-panel name="comments">
            <Comments />
          </q-tab-panel>
        </q-tab-panels>
      </template>
    </q-splitter>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { useMeta } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
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
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const $navStore = useNavStore();
    const { loading, success, data, fetchAPI } = apiInterface();
    const source = ref({});

    const id = inject("id");

    const splitterModel = ref(10);
    const tab = ref("attributes");
    const hasAttributes = computed(() => !isNil(source.value.attributes));
    const hasAgents = computed(() => notNully(source.value.agents));
    const hasChildren = computed(() => notNully(source.value.children));
    const hasPlaces = computed(() => notNully(source.value.places));
    const hasPages = computed(() => notNully(source.value.pages));

    provide("model", "Source");
    provide("source", source);
    provide("hasAttributes", hasAttributes);

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
      hasAgents,
      hasAttributes,
      hasChildren,
      hasPages,
      hasPlaces,
      loading,
      splitterModel,
      tab,
    };
  },
});
</script>
