<template>
  <div class="full-width full-height q-px-content-visual">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!ui.globalLoading">
                  {{ record.name }}
                  <TagWidget
                    v-if="record.hasInventory"
                    name="list"
                    colour="green-1"
                    textColour="green-8"
                    size="xs"
                    module="standalone"
                    class="q-ml-sm"
                  />
                </template>
                <q-skeleton v-else width="350px" height="30px" type="rect" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!ui.globalLoading">
                  <span>Created</span>
                  {{ formatDate(record.creationTimestamp) }} by
                  <DetailPopover
                    :userData="{
                      username: record.creationUser.username,
                      fullName: record.creationUser.fullName,
                    }"
                    :showAvatar="false"
                  />
                  <span>, last modified</span>
                  {{ formatDate(record.modificationTimestamp) }} by
                  <DetailPopover
                    :userData="{
                      username: record.modificationUser.username,
                      fullName: record.modificationUser.fullName,
                    }"
                    :showAvatar="false"
                  />
                </template>
                <q-skeleton v-else width="500px" height="12px" type="rect" />
              </div>
            </div>
          </div>
        </transition>
        <div class="row">
          <q-tabs
            v-model="view.tab"
            dense
            no-caps
            inline-label
            switch-indicator
            align="left"
            class="bg-white text-grey-8 tab-container"
            active-class="active-tab"
          >
            <q-tab name="info" icon="o_info" label="Info" />
            <template v-if="!ui.globalLoading">
              <q-tab v-if="hasChildren" name="children" label="Children" icon="o_account_tree">
                <q-badge
                  color="indigo-1"
                  rounded
                  class="text-grey-8 q-mx-xs"
                  :label="record.children.length"
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
                  :label="record.pages.length"
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
            </template>
            <q-spinner-oval v-else size="sm" class="q-ml-md" />
          </q-tabs>
        </div>
      </div>
      <template v-if="!ui.globalLoading">
        <div v-if="resource === 'record'" class="col-auto record-actions">
          <div class="row transition-all">
            <div class="row q-mr-sm">
              <BooleanWidget
                v-if="resource === 'record'"
                :value="record && !record.workflow.isPublic"
                :onlyTrue="true"
                trueIcon="public"
                trueColour="light-green-7"
              />
              <BooleanWidget
                v-if="resource === 'record'"
                :value="record && !record.workflow.helpFlag"
                :onlyTrue="true"
                trueIcon="flag"
                trueColour="red-4"
                class="q-ml-xs"
              />
            </div>
            <WorkflowManager :data="record.workflow" />
          </div>
        </div>
      </template>
    </div>
    <div class="row q-pt-sm">
      <div class="col">
        <template v-if="!ui.globalLoading">
          <q-tab-panels
            v-model="view.tab"
            animated
            transition-prev="jump-up"
            transition-next="jump-up"
            keep-alive
          >
            <q-tab-panel name="info" class="q-pt-none q-px-none">
              <RecordAttributes />
            </q-tab-panel>
            <q-tab-panel name="children" class="q-pt-none q-px-none">
              <RecordChildren :children="record.children" />
            </q-tab-panel>
            <q-tab-panel name="folios" class="q-pt-sm q-px-none">
              <RecordPages :pages="record.pages" />
            </q-tab-panel>
            <q-tab-panel name="entities" class="q-pt-none q-px-none">
              <div v-if="hasAgents">
                <RecordAgents :agents="record.agents" />
              </div>
              <div v-if="hasPlaces" class="q-mt-md">
                <RecordPlaces :places="record.places" />
              </div>
            </q-tab-panel>
            <q-tab-panel name="comments" class="q-pt-md q-px-lg">
              <CommentWidget @on-count-changed="updateCommentCount" />
            </q-tab-panel>
            <q-tab-panel name="log" class="q-pt-md q-px-lg">
              <LogViewer :data="record.workflow" />
            </q-tab-panel>
          </q-tab-panels>
        </template>
        <AdaptiveSpinner v-else />
      </div>
    </div>
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { useAPI, useEditing, useStores } from "@/use";
import {
  AdaptiveSpinner,
  BooleanWidget,
  CommentWidget,
  DetailPopover,
  LogViewer,
  TagWidget,
  WorkflowManager,
} from "@/components";
import { formatDate, notNully } from "@/utils";
import RecordAttributes from "./RecordAttributes.vue";
import RecordAgents from "./RecordAgents.vue";
import RecordChildren from "./RecordChildren.vue";
import RecordPages from "./RecordPages.vue";
import RecordPlaces from "./RecordPlaces.vue";

export default defineComponent({
  name: "RecordDetail",
  components: {
    AdaptiveSpinner,
    BooleanWidget,
    DetailPopover,
    CommentWidget,
    LogViewer,
    RecordAttributes,
    RecordAgents,
    RecordChildren,
    RecordPages,
    RecordPlaces,
    TagWidget,
    WorkflowManager,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const { ui, view } = useStores();
    const { success, data, fetchAPI } = apiInterface();
    const record = ref({});
    const id = ref($route.params.id);
    const hasAttributes = computed(() => notNully(record.value.attributes));
    const hasAgents = computed(() => notNully(record.value.agents));
    const hasChildren = computed(() => notNully(record.value.children));
    const hasPlaces = computed(() => notNully(record.value.places));
    const hasPages = computed(() => notNully(record.value.pages));
    const entityCount = computed(() => {
      let agentsCount = hasAgents.value ? record.value.agents.length : 0;
      let placesCount = hasPlaces.value ? record.value.places.length : 0;
      return agentsCount + placesCount;
    });
    const commentCount = ref(0);

    provide("model", "Record");
    provide("id", id);
    provide("record", record);
    provide("hasAttributes", hasAttributes);
    provide("hasPages", hasPages);
    provide("hasChildren", hasChildren);
    provide("hasAgents", hasAgents);
    provide("hasPlaces", hasPlaces);

    useMeta(() => ({
      title: record.value ? record.value.name : `Record ${id.value}`,
    }));

    // const fetchData = async () => {
    //   ui.globalLoading = true;
    //   await fetchAPI(requests.records.getRecord(id.value));
    //   if (success.value)
    //     await recordDetailSchema
    //       .validate(data.value, { stripUnknown: true })
    //       .then((value) => {
    //         resource.value =
    //           {
    //             archive: "archive",
    //             "file unit": "archivalFile",
    //             record: "record",
    //           }[value.type.name.toLowerCase()] || "bibliography";
    //         record.value = value;
    //         commentCount.value = value.commentCount;
    //         nav.currentSubsection = value.type.name + "s";
    //         nav.breadcrumbTail.push(value.shortName);
    //         ui.globalLoading = false;
    //       });
    // };

    const fetchData = async () => {
      ui.globalLoading = true;
      await fetchAPI(requests.records.getRecord(id.value));
      if (success.value) {
        resource.value = "record";
        record.value = data.value;
        commentCount.value = data.value.commentCount;
        ui.breadcrumbTail.push(data.value.shortName);
        ui.globalLoading = false;
      }
    };

    const updateCommentCount = (cnt) => {
      commentCount.value = cnt;
    };

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          id.value = to;
          ui.resetBreadcrumbTail();
          await fetchData();
        }
      },
      { immediate: true, flush: "post" },
    );

    editingDetailRouteGuard();

    return {
      commentCount,
      updateCommentCount,
      view,
      entityCount,
      formatDate,
      hasAgents,
      hasAttributes,
      hasChildren,
      hasPages,
      hasPlaces,
      resource,
      record,
      ui,
    };
  },
});
</script>

<style lang="scss">
.record-actions {
  border-bottom: 1px solid #d1d1d1;
  margin-top: auto;
  padding-bottom: 6px;
}
</style>
