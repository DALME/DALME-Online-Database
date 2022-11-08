<template>
  <div v-if="!loading">
    <div class="row">
      <div class="col-grow q-py-lg">
        <div class="row items-center text-h5">
          {{ source.name }}
          <Tag
            v-if="source.hasInventory"
            name="list"
            colour="green-1"
            textColour="green-8"
            size="xs"
            module="standalone"
            class="q-ml-sm"
          />
        </div>
        <div class="row detail-row-subheading text-grey-8">
          <span>Created</span> {{ formatDate(source.created.timestamp) }} by
          <DetailPopover
            :userData="{
              username: source.created.username,
              fullName: source.created.user,
            }"
            :showAvatar="false"
          />
          <span>, last modified</span>
          {{ formatDate(source.modified.timestamp) }} by
          <DetailPopover
            :userData="{
              username: source.modified.username,
              fullName: source.modified.user,
            }"
            :showAvatar="false"
          />
        </div>
      </div>
      <div v-if="resource === 'record'" class="col-auto q-py-lg">
        <WorkflowManager :data="source.workflow" />
      </div>
    </div>
    <div class="row">
      <q-tabs
        v-model="tab"
        dense
        no-caps
        inline-label
        switch-indicator
        align="left"
        class="bg-white text-grey-8 tab-container"
        active-class="active-tab"
      >
        <q-tab name="info" icon="o_info" label="Info" />
        <q-tab
          v-if="hasChildren"
          name="children"
          label="Children"
          icon="o_account_tree"
        >
          <q-badge
            color="indigo-1"
            rounded
            class="text-grey-8 q-mx-xs"
            :label="source.children.length"
          />
        </q-tab>
        <q-tab
          v-if="hasPages"
          name="folios"
          label="Folios"
          icon="o_import_contacts"
          class="side-tab"
        >
          <q-badge
            color="indigo-1"
            rounded
            class="text-grey-8 q-mx-xs"
            :label="source.pages.length"
          />
        </q-tab>
        <q-tab
          v-if="hasAgents || hasPlaces"
          name="entities"
          label="Entities"
          icon="o_person_pin_circle"
          class="side-tab"
        >
          <q-badge
            color="indigo-1"
            rounded
            class="text-grey-8 q-mx-xs"
            :label="entityCount"
          />
        </q-tab>
        <q-tab name="comments" icon="o_forum" label="Discussion">
          <q-badge
            v-if="commentCount > 0"
            color="indigo-1"
            rounded
            class="text-grey-8 q-mx-xs"
            :label="commentCount"
          />
        </q-tab>
        <q-tab name="log" icon="o_work_history" label="Work Log" />
        <q-space />
        <BooleanIcon
          v-if="resource === 'record'"
          :value="source.workflow.isPublic"
          :onlyTrue="true"
          trueIcon="public"
          trueColour="light-green-7"
        />
        <BooleanIcon
          v-if="resource === 'record'"
          :value="source.workflow.helpFlag"
          :onlyTrue="true"
          trueIcon="flag"
          trueColour="red-4"
          class="q-ml-xs"
        />
      </q-tabs>
    </div>
    <div class="row q-pt-sm">
      <div class="col">
        <q-tab-panels
          v-model="tab"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="info" class="q-pt-none q-px-none">
            <SourceAttributes />
          </q-tab-panel>
          <q-tab-panel name="children" class="q-pt-none q-px-none">
            <SourceChildren :children="source.children" />
          </q-tab-panel>
          <q-tab-panel name="folios" class="q-pt-none q-px-none">
            <SourcePages :pages="source.pages" />
          </q-tab-panel>
          <q-tab-panel name="entities" class="q-pt-none q-px-none">
            <div v-if="hasAgents">
              <SourceAgents :agents="source.agents" />
            </div>
            <div v-if="hasPlaces" class="q-mt-md">
              <SourcePlaces :places="source.places" />
            </div>
          </q-tab-panel>
          <q-tab-panel name="comments" class="q-pt-md q-px-lg">
            <Comments />
          </q-tab-panel>
          <q-tab-panel name="log" class="q-pt-md q-px-lg">
            <LogViewer :data="source.workflow" />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { useNavStore } from "@/stores/navigation";
import { requests } from "@/api";
import { sourceDetailSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";
import {
  BooleanIcon,
  DetailPopover,
  formatDate,
  notNully,
  OpaqueSpinner,
  Tag,
} from "@/components/utils";
import { Comments, LogViewer, WorkflowManager } from "@/components";
import SourceAttributes from "./SourceAttributes.vue";
import SourceAgents from "./SourceAgents.vue";
import SourceChildren from "./SourceChildren.vue";
import SourcePages from "./SourcePages.vue";
import SourcePlaces from "./SourcePlaces.vue";

export default defineComponent({
  name: "SourceDetail",
  components: {
    AdaptiveSpinner,
    BooleanIcon,
    DetailPopover,
    Comments,
    LogViewer,
    SourceAttributes,
    SourceAgents,
    SourceChildren,
    SourcePages,
    SourcePlaces,
    Tag,
    WorkflowManager,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const { nav, ui } = useStores();
    ui.mergeValues({
      view: {
        tab: "info",
      },
    });
    const { success, data, fetchAPI } = apiInterface();
    const source = ref({});

    const id = inject("id");

    const tab = ref("info");
    const hasAttributes = computed(() => notNully(source.value.attributes));
    const hasAgents = computed(() => notNully(source.value.agents));
    const hasChildren = computed(() => notNully(source.value.children));
    const hasPlaces = computed(() => notNully(source.value.places));
    const hasPages = computed(() => notNully(source.value.pages));
    const entityCount = computed(() => {
      let agentsCount = hasAgents.value ? source.value.agents.length : 0;
      let placesCount = hasPlaces.value ? source.value.places.length : 0;
      return agentsCount + placesCount;
    });
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
            $navStore.breadcrumbTail.push(value.shortName);
            loading.value = false;
          });
    };

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          id.value = to;
          $navStore.resetBreadcrumbTail();
          await fetchData();
        }
      },
      { immediate: true },
    );

    editingDetailRouteGuard();

    onBeforeRouteLeave(() => {
      $navStore.resetBreadcrumbTail();
    });

    return {
      commentCount,
      entityCount,
      formatDate,
      hasAgents,
      hasAttributes,
      hasChildren,
      hasPages,
      hasPlaces,
      loading,
      resource,
      source,
      tab,
    };
  },
});
</script>
