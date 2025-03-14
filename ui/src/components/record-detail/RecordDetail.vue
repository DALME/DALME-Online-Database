<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div class="info-area row" v-if="showInfoArea && !ui.globalLoading">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!ui.globalLoading">
                  {{ recordData.name.value }}
                  <TagPill
                    v-if="workflowData.isPublic"
                    name="public"
                    colour="green-1"
                    textColour="green-8"
                    size="sm"
                    module="standalone"
                    class="q-ml-md q-mt-xs"
                  />
                </template>
                <q-skeleton v-else width="350px" height="30px" type="rect" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!ui.globalLoading">
                  <span
                    >Created on {{ recordData.creationTimestamp.value.date }} @
                    {{ recordData.creationTimestamp.value.time }} by
                  </span>
                  <UserPill
                    :user="recordData.creationUser.value"
                    text-size="12px"
                    :show-avatar="false"
                    inline
                  />
                  <span
                    >, last modified on {{ recordData.modificationTimestamp.value.date }} @
                    {{ recordData.modificationTimestamp.value.time }} by
                  </span>
                  <UserPill
                    :user="recordData.modificationUser.value"
                    text-size="12px"
                    :show-avatar="false"
                    inline
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
              <q-tab
                v-if="pageData.length"
                name="pages"
                label="Folios"
                icon="o_import_contacts"
                class="side-tab"
              >
                <q-badge
                  color="indigo-1"
                  rounded
                  class="text-grey-8 q-mx-xs"
                  :label="pageData.length"
                />
              </q-tab>
              <q-tab
                v-if="agentData.length"
                name="entities"
                label="Entities"
                icon="o_person_pin_circle"
                class="side-tab"
              >
                <q-badge
                  color="indigo-1"
                  rounded
                  class="text-grey-8 q-mx-xs"
                  :label="agentData.length"
                />
              </q-tab>
              <q-tab name="comments" icon="o_forum" label="Discussion & Activity">
                <q-badge
                  v-if="commentCount > 0"
                  color="indigo-5"
                  rounded
                  class="text-indigo-1 q-mx-xs"
                  :label="commentCount"
                />
              </q-tab>
            </template>
            <AdaptiveSpinner v-else type="bars" size="sm" class="q-ml-md" />
          </q-tabs>
        </div>
      </div>
      <template v-if="!ui.globalLoading">
        <div class="col-auto record-actions">
          <div class="row transition-all">
            <div class="row q-mr-sm">
              <BooleanValue
                :value="workflowData.helpFlag"
                :onlyTrue="true"
                trueIcon="flag"
                trueColour="red-4"
                class="q-ml-xs"
              />
            </div>
            <WorkflowManager
              v-if="auth.user.isAdmin"
              :data="workflowData"
              @state-changed="updateWorkflow"
            />
            <q-btn
              v-if="view.tab === 'pages'"
              dense
              outline
              size="sm"
              :icon="showInfoArea ? 'mdi-arrow-collapse-vertical' : 'mdi-arrow-expand-vertical'"
              text-color="grey-7"
              class="bg-grey-2 q-ml-xs"
              @click="showInfoArea = !showInfoArea"
            />
          </div>
        </div>
      </template>
    </div>
    <div class="row q-pt-sm content-container-row">
      <div class="col content-container">
        <template v-if="!ui.globalLoading">
          <q-tab-panels
            v-model="view.tab"
            animated
            transition-prev="jump-up"
            transition-next="jump-up"
            keep-alive
          >
            <q-tab-panel name="info" class="q-pt-none q-px-none">
              <div class="col-9 q-pr-lg q-pt-md">
                <template v-if="ui.windowWidth > 1100">
                  <div class="row no-wrap">
                    <div class="col-6 q-mr-md">
                      <DetailCard
                        icon="bookmark"
                        title="Record"
                        pad-container
                        :fields="fieldPlacements.infocard"
                        :data="recordData"
                        :register="registerComponent"
                        @value-changed="onValueChange"
                      />
                    </div>
                    <div class="col-6">
                      <DetailCard
                        :ref="(el) => registerComponent(recordData.description.name, el)"
                        :field-name="recordData.description.name"
                        icon="subject"
                        title="Description"
                        noData="No description assigned."
                        :data="recordData.description"
                        markdown
                        editable
                        @value-changed="onValueChange"
                      />

                      <DetailCard
                        v-if="pageData.length"
                        icon="auto_stories"
                        title="Folios"
                        showFilter
                        class="q-mt-md"
                        @value-changed="onValueChange"
                      >
                        <RecordPages overview :pages="pageData" />
                      </DetailCard>

                      <DetailCard
                        v-if="agentData.length"
                        icon="people"
                        title="Agents"
                        showFilter
                        class="q-mt-md"
                        @value-changed="onValueChange"
                      >
                        <RecordAgents overview :agents="agentData" />
                      </DetailCard>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <DetailCard
                    icon="bookmark"
                    title="Record"
                    pad-container
                    :fields="fieldPlacements.infocard"
                    :data="recordData"
                    :register="registerComponent"
                    @value-changed="onValueChange"
                  />

                  <DetailCard
                    :ref="(el) => registerComponent(recordData.description.name, el)"
                    :field-name="recordData.description.name"
                    icon="subject"
                    title="Description"
                    noData="No description assigned."
                    class="q-mt-md"
                    :data="recordData.description"
                    markdown
                    editable
                    @value-changed="onValueChange"
                  />

                  <DetailCard
                    v-if="pageData.length"
                    icon="auto_stories"
                    title="Folios"
                    showFilter
                    class="q-mt-md"
                    @value-changed="onValueChange"
                  >
                    <RecordPages overview :pages="pageData" />
                  </DetailCard>

                  <DetailCard
                    v-if="agentData.length"
                    icon="people"
                    title="Agents"
                    showFilter
                    class="q-mt-md"
                    @value-changed="onValueChange"
                  >
                    <RecordAgents overview :agents="agentData" />
                  </DetailCard>
                </template>
              </div>
            </q-tab-panel>
            <q-tab-panel name="pages" class="q-pt-sm q-px-none editor-panel">
              <RecordPages :pages="pageData" />
            </q-tab-panel>
            <q-tab-panel name="entities" class="q-pt-none q-px-none">
              <div v-if="agentData.length">
                <RecordAgents :agents="agentData" />
              </div>
            </q-tab-panel>
            <q-tab-panel name="comments" class="q-pt-md q-px-lg">
              <CommentBox @on-count-changed="updateCommentCount" :worklog="workflowData.workLog" />
            </q-tab-panel>
          </q-tab-panels>
        </template>
        <AdaptiveSpinner v-else />
      </div>
      <div v-if="!ui.globalLoading && view.tab !== 'pages'" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar :fields="fieldPlacements.sidebar" :data="recordData">
          <template v-slot:extraElements>
            <DetailElement v-if="collectionData.length" label="Collections">
              <template v-slot:content>
                <template v-for="collection in collectionData" :key="collection.id">
                  <q-chip
                    clickable
                    color="deep-purple-6"
                    text-color="white"
                    size="sm"
                    icon="mdi-folder-outline"
                    outline
                  >
                    {{ collection.name }}
                  </q-chip>
                </template>
              </template>
            </DetailElement>
            <DetailElement label="Created">
              <template v-slot:content>
                <div>
                  <UserPill
                    :user="recordData.creationUser.value"
                    text-size="13px"
                    :bold="false"
                    :show-avatar="false"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ recordData.creationTimestamp.value.date }} @
                    {{ recordData.modificationTimestamp.value.time }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template v-slot:content>
                <div>
                  <UserPill
                    :user="recordData.modificationUser.value"
                    text-size="13px"
                    :bold="false"
                    :show-avatar="false"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ recordData.modificationTimestamp.value.date }} @
                    {{ recordData.modificationTimestamp.value.time }}
                  </div>
                </div>
              </template>
            </DetailElement>
          </template>
        </DetailSidebar>
      </div>
    </div>
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { useAPI, useEditing, useEventHandling, useStores } from "@/use";
import {
  AdaptiveSpinner,
  BooleanValue,
  CommentBox,
  DetailCard,
  DetailSidebar,
  DetailElement,
  TagPill,
  WorkflowManager,
  UserPill,
} from "@/components";
import { nully, isObject } from "@/utils";
import RecordAgents from "./RecordAgents.vue";
import RecordPages from "./RecordPages.vue";
import { metadata } from "./metadata.js";
import { recordDetailSchema, workflowSchema, attributeSchema } from "@/schemas";
import { snakeCase } from "change-case";

export default defineComponent({
  name: "RecordDetail",
  components: {
    AdaptiveSpinner,
    BooleanValue,
    CommentBox,
    DetailCard,
    DetailElement,
    DetailSidebar,
    RecordAgents,
    RecordPages,
    TagPill,
    UserPill,
    WorkflowManager,
  },
  setup() {
    const $route = useRoute();
    const { notifier } = useEventHandling();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const { auth, ui, view } = useStores();
    const { success, data, fetchAPI } = apiInterface();
    const id = ref($route.params.id);
    const refRegister = ref({});
    const isPrivate = ref(false);
    const commentCount = ref(0);
    const folioCount = ref(0);
    const recordData = ref({});
    const agentData = ref([]);
    const pageData = ref([]);
    const collectionData = ref([]);
    const workflowData = ref({});
    const fieldPlacements = ref({
      sidebar: [],
      infocard: [],
      standalone: [],
    });

    const showInfoArea = ref(true);

    provide("model", "Record");
    provide("id", id);
    provide("showInfoArea", showInfoArea);

    useMeta(() => ({
      title: !nully(recordData.value) ? recordData.value.name.value : `Record ${id.value}`,
    }));

    const fetchData = async () => {
      ui.globalLoading = true;
      await fetchAPI(requests.records.getRecord(id.value));
      if (success.value) {
        await recordDetailSchema.validate(data.value, { stripUnknown: false }).then((validated) => {
          const dataset = {};
          for (const [key, payload] of Object.entries(metadata)) {
            if (payload.source == "attribute") {
              let attr = validated.attributes.filter((x) => x.name == key);
              if (attr.length) {
                if (attr.length > 1 || !attr[0].isUnique) {
                  attr = {
                    dataType: attr[0].dataType,
                    label: attr[0].label,
                    value: attr,
                  };
                } else {
                  attr = attr[0];
                }
                attr["name"] = key;
                dataset[key] = Object.assign(payload, attr);
                if (payload.show) fieldPlacements.value[payload.placement].push(key);
              } else if (payload.show) {
                dataset[key] = Object.assign(payload, { value: null, name: key });
                if (payload.show) fieldPlacements.value[payload.placement].push(key);
              }
            } else if (payload.source != "standalone" && (payload.show || key in validated)) {
              dataset[key] = Object.assign(payload, { value: validated[key], name: key });
              if (payload.show) fieldPlacements.value[payload.placement].push(key);
            }
          }
          resource.value = "record";
          isPrivate.value = validated.isPrivate;
          commentCount.value = validated.commentCount;
          folioCount.value = validated.noFolios;
          recordData.value = dataset;
          agentData.value = validated.agents || [];
          pageData.value = validated.pages;
          collectionData.value = validated.collections;
          workflowData.value = validated.workflow;
          ui.breadcrumbTail.push(validated.shortName);
          ui.globalLoading = false;
          console.log("recordData", recordData.value);
        });
      }
    };

    const updateCommentCount = (cnt) => {
      commentCount.value = cnt;
    };

    const registerComponent = (name, reference) => {
      refRegister.value[name] = reference;
    };

    const updateWorkflow = async (newState) => {
      await fetchAPI(requests.workflow.changeState(id.value, newState));
      if (success.value) {
        await workflowSchema.validate(data.value, { stripUnknown: false }).then((value) => {
          workflowData.value = value;
        });
      } else {
        notifier.workflow.updateFailed();
      }
    };

    const editHandlers = (payload) => {
      if (payload.source === "attribute") {
        const request = payload.update
          ? requests.attributes.updateAttributeValue(payload.id, payload.value)
          : requests.records.addAttribute(id.value, snakeCase(payload.name), payload.value);
        const notifier = (name) =>
          payload.update
            ? notifier.attributes.updateFailed(name)
            : notifier.records.addAttributeFailed(name);
        const handler = (name, value, _restore) =>
          (recordData.value[name] = Object.assign(recordData.value[name], value));
        const schema = attributeSchema;
        return { request, notifier, handler, schema };
      } else {
        const request =
          payload.source === "field"
            ? requests.records.editRecord(
                id.value,
                { [snakeCase(payload.name)]: payload.value },
                true,
              )
            : requests.records.updateRelated(
                id.value,
                snakeCase(payload.name),
                isObject(payload.value) ? payload.value.value : payload.value,
              );
        const notifier = (name) => notifier.records.fieldUpdateFailed(name);
        const handler = (name, value, _restore) =>
          (recordData.value[name].value = _restore ? value : value[name]);
        const schema = recordDetailSchema;
        return { request, notifier, handler, schema };
      }
    };

    const onValueChange = async (payload) => {
      console.log("onValueChange", payload);
      refRegister.value[payload.name].saving = true;
      const handlers = editHandlers(payload);

      await fetchAPI(handlers.request);
      if (success.value) {
        await handlers.schema.validate(data.value, { stripUnknown: false }).then((value) => {
          handlers.handler(payload.name, value, false);
          refRegister.value[payload.name].saving = false;
        });
      } else {
        handlers.notifier(payload.name);
        handlers.handler(payload.name, payload.oldValue, true);
        refRegister.value[payload.name].saving = false;
      }
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
      resource,
      recordData,
      agentData,
      pageData,
      collectionData,
      workflowData,
      ui,
      updateWorkflow,
      auth,
      fieldPlacements,
      registerComponent,
      onValueChange,
      showInfoArea,
    };
  },
});
</script>

<style lang="scss" scoped>
.record-actions {
  border-bottom: 1px solid #d1d1d1;
  margin-top: auto;
  padding-bottom: 6px;
}
</style>
