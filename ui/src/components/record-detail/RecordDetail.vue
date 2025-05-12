<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div v-if="showInfoArea && !loading" class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!loading">
                  {{ recordData.name.value }}
                  <TagPill
                    v-if="workflowData.isPublic"
                    class="q-ml-md q-mt-xs"
                    colour="green-1"
                    module="standalone"
                    name="public"
                    size="sm"
                    text-colour="green-8"
                  />
                </template>
                <q-skeleton v-else height="30px" type="rect" width="350px" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!loading">
                  <span>
                    Created on
                    {{ formatDate(recordData.creationTimestamp.value, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordData.creationUser.value"
                    text-size="12px"
                    inline
                  />
                  <span
                    >, last modified on
                    {{ formatDate(recordData.modificationTimestamp.value, "DATETIME_AT") }}
                    by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordData.modificationUser.value"
                    text-size="12px"
                    inline
                  />
                </template>
                <q-skeleton v-else height="12px" type="rect" width="500px" />
              </div>
            </div>
          </div>
        </transition>
        <div class="row">
          <q-tabs
            v-model="view.tab"
            active-class="active-tab"
            align="left"
            class="bg-white text-grey-8 tab-container"
            dense
            inline-label
            no-caps
            switch-indicator
          >
            <q-tab icon="o_info" label="Info" name="info" />
            <template v-if="!loading">
              <q-tab
                v-if="pageData.length"
                class="side-tab"
                icon="o_import_contacts"
                label="Folios"
                name="pages"
              >
                <q-badge
                  :label="pageData.length"
                  class="text-grey-8 q-mx-xs"
                  color="indigo-1"
                  rounded
                />
              </q-tab>
              <q-tab
                v-if="entityCount > 0"
                class="side-tab"
                icon="o_person_pin_circle"
                label="Entities"
                name="entities"
              >
                <q-badge
                  :label="entityCount"
                  class="text-grey-8 q-mx-xs"
                  color="indigo-1"
                  rounded
                />
              </q-tab>
              <q-tab icon="o_forum" label="Discussion & Activity" name="comments">
                <q-badge
                  v-if="commentCount > 0"
                  :label="commentCount"
                  class="text-indigo-1 q-mx-xs"
                  color="indigo-5"
                  rounded
                />
              </q-tab>
            </template>
            <AdaptiveSpinner v-else class="q-ml-md" color="indigo-3" size="xs" />
          </q-tabs>
        </div>
      </div>
      <template v-if="!loading">
        <div class="col-auto record-actions">
          <div class="row transition-all">
            <div class="row q-mr-sm">
              <BooleanValue
                :only-true="true"
                :value="workflowData.helpFlag"
                class="q-ml-xs"
                true-colour="red-4"
                true-icon="flag"
              />
            </div>
            <WorkflowManager
              v-if="auth.user.isAdmin"
              @state-changed="updateWorkflow"
              :data="workflowData"
            />
            <q-btn
              v-if="showEditBtn"
              @click="eventBus.emit('toggleEditor')"
              :icon="editOn ? 'mdi-pencil-off' : 'mdi-pencil'"
              class="bg-grey-2 q-ml-xs"
              size="sm"
              text-color="grey-7"
              dense
              outline
            />
          </div>
        </div>
      </template>
    </div>
    <div class="row q-pt-sm content-container-row">
      <div class="col content-container">
        <template v-if="!loading">
          <q-tab-panels v-model="view.tab" animated keep-alive>
            <q-tab-panel class="q-pt-none q-px-none" name="info">
              <div class="col-9 q-pr-lg q-pt-md">
                <template v-if="ui.windowWidth > 1100">
                  <div class="row no-wrap">
                    <div class="col-6 q-mr-md">
                      <DetailCard
                        @value-changed="onValueChange"
                        :data="recordData"
                        :fields="fieldPlacements.infocard"
                        :register="registerComponent"
                        icon="bookmark"
                        title="Record"
                        pad-container
                      />
                    </div>
                    <div class="col-6">
                      <DetailCard
                        :ref="(el) => registerComponent(recordData.description.name, el)"
                        @value-changed="onValueChange"
                        :data="recordData.description"
                        :field-name="recordData.description.name"
                        icon="subject"
                        no-data="No description assigned."
                        title="Description"
                        editable
                        markdown
                      />

                      <DetailCard
                        v-if="pageData.length"
                        @value-changed="onValueChange"
                        class="q-mt-md"
                        icon="auto_stories"
                        title="Folios"
                        show-filter
                      >
                        <RecordPages :pages="pageData" />
                      </DetailCard>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <DetailCard
                    @value-changed="onValueChange"
                    :data="recordData"
                    :fields="fieldPlacements.infocard"
                    :register="registerComponent"
                    icon="bookmark"
                    title="Record"
                    pad-container
                  />

                  <DetailCard
                    :ref="(el) => registerComponent(recordData.description.name, el)"
                    @value-changed="onValueChange"
                    :data="recordData.description"
                    :field-name="recordData.description.name"
                    class="q-mt-md"
                    icon="subject"
                    no-data="No description assigned."
                    title="Description"
                    editable
                    markdown
                  />

                  <DetailCard
                    v-if="pageData.length"
                    @value-changed="onValueChange"
                    class="q-mt-md"
                    icon="auto_stories"
                    title="Folios"
                    show-filter
                  >
                    <RecordPages :pages="pageData" />
                  </DetailCard>
                </template>
              </div>
            </q-tab-panel>
            <q-tab-panel class="q-pt-sm q-px-none editor-panel" name="pages">
              <RecordEditor />
            </q-tab-panel>

            <q-tab-panel class="q-pt-none q-px-none" name="entities">
              <div class="col-9 q-pr-sm">
                <DetailCard
                  v-if="agentData.length"
                  @value-changed="onValueChange"
                  class="q-mt-md"
                  icon="people"
                  title="Agents"
                  show-filter
                >
                  <RecordAgents :agents="agentData" />
                </DetailCard>

                <DetailCard
                  v-if="placeData.length"
                  @value-changed="onValueChange"
                  class="q-mt-md"
                  icon="mdi-map-marker"
                  title="Places"
                  show-filter
                >
                  <RecordPlaces :places="placeData" />
                </DetailCard>
              </div>
            </q-tab-panel>

            <q-tab-panel class="q-pt-md q-px-lg" name="comments">
              <CommentBox @on-count-changed="updateCommentCount" :worklog="workflowData.workLog" />
            </q-tab-panel>
          </q-tab-panels>
        </template>
        <AdaptiveSpinner
          v-else
          color="indigo-5"
          left="0"
          position="absolute"
          size="50px"
          top="0"
          type="hourglass"
          adaptive
        />
      </div>
      <div v-if="!ui.globalLoading && view.tab !== 'pages'" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar :data="recordData" :fields="fieldPlacements.sidebar">
          <template #extraElements>
            <DetailElement v-if="collectionData.length" label="Collections">
              <template #content>
                <template v-for="collection in collectionData" :key="collection.id">
                  <q-chip
                    color="deep-purple-6"
                    icon="mdi-folder-outline"
                    size="sm"
                    text-color="white"
                    clickable
                    outline
                  >
                    {{ collection.name }}
                  </q-chip>
                </template>
              </template>
            </DetailElement>
            <DetailElement label="Created">
              <template #content>
                <div>
                  <UserPill
                    :bold="false"
                    :show-avatar="false"
                    :user="recordData.creationUser.value"
                    text-size="13px"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ formatDate(recordData.creationTimestamp.value, "DATETIME_AT") }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template #content>
                <div>
                  <UserPill
                    :bold="false"
                    :show-avatar="false"
                    :user="recordData.modificationUser.value"
                    text-size="13px"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ formatDate(recordData.modificationTimestamp.value, "DATETIME_AT") }}
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
import { snakeCase } from "change-case";
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import {
  AdaptiveSpinner,
  BooleanValue,
  CommentBox,
  DetailCard,
  DetailElement,
  DetailSidebar,
  RecordEditor,
  TagPill,
  UserPill,
  WorkflowManager,
} from "@/components";
import { attributeSchema, recordDetailSchema, workflowSchema } from "@/schemas";
import { useAPI, useEditing, useEventHandling, useStores } from "@/use";
import { formatDate, getColumns, isObject, nully } from "@/utils";

import { metadata } from "./metadata.js";
import { columnMap } from "./pageColumns";
import RecordAgents from "./RecordAgents.vue";
import RecordPages from "./RecordPages.vue";
import RecordPlaces from "./RecordPlaces.vue";

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
    RecordEditor,
    RecordPages,
    RecordPlaces,
    TagPill,
    UserPill,
    WorkflowManager,
  },
  setup() {
    const $route = useRoute();
    const { eventBus, notifier } = useEventHandling();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();
    const { auth, ui, view, views, showEditBtn, showInfoArea, editOn } = useStores();
    const { success, data, fetchAPI } = apiInterface();
    const id = ref($route.params.id);
    const pageColumns = ref(getColumns(columnMap));
    const refRegister = ref({});
    const isPrivate = ref(false);
    const commentCount = ref(0);
    const folioCount = ref(0);
    const recordData = ref({});
    const agentData = ref([]);
    const pageData = ref([]);
    const placeData = ref([]);
    const collectionData = ref([]);
    const workflowData = ref({});
    const fieldPlacements = ref({
      sidebar: [],
      infocard: [],
      standalone: [],
    });

    const entityCount = computed(() => agentData.value.length + placeData.value.length);

    useMeta(() => ({
      title: !nully(recordData.value) ? recordData.value.name.value : `Record ${id.value}`,
    }));

    const getPages = (pages) => {
      pages.forEach((page, idx) => {
        page.ref = idx;
        page.editorTab = "preview";
        page.dbTei = page.transcription?.transcription;
        page.tei = page.transcription?.transcription;
        page.viewerZoom = 0;
      });
      return pages;
    };

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
          placeData.value =
            validated.places?.map((p) => Object.assign(p, formatLocation(p.location))) || [];
          collectionData.value = validated.collections;
          workflowData.value = validated.workflow;
          ui.breadcrumbTail.push(validated.shortName);

          views.mergeValues(views, {
            pages: getPages(pageData.value),
            currentPageRef: 0,
            pageDrawerMini: true,
            showTagMenu: false,
            splitterHorizontal: true,
            editorSplitter: 0,
            lastSplitter: 0,
            editOn: false,
          });

          ui.globalLoading = false;
          // console.log("recordData", recordData.value);
          // console.log(agentData.value);
          // console.log(pageData.value);
          // console.log(placeData.value);
          // console.log(collectionData.value);
          // console.log(workflowData.value);
        });
      }
    };

    const formatLocation = (loc) => {
      if (loc.locationType == "Locale") {
        const locale = loc.attributes.filter((x) => x.name == "locale");
        const name = locale[0].value.name;
        const region = locale[0].value.administrativeRegion;
        const country = locale[0].value.country.name;
        const lat = locale[0].value.latitude;
        const lon = locale[0].value.longitude;
        return {
          locationName: name,
          locationRegion: region,
          locationCountry: country,
          latitude: lat,
          longitude: lon,
          locationDetail: `${name}, ${region} (${country})`,
          locationGeometry: `POINT (${lon}, ${lat})`,
        };
      } else {
        return {};
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

    provide("model", "Record");
    provide("id", id);
    provide("pages", pageData.value);
    provide("pageColumns", pageColumns);

    return {
      commentCount,
      updateCommentCount,
      view,
      resource,
      recordData,
      agentData,
      pageData,
      placeData,
      collectionData,
      workflowData,
      ui,
      updateWorkflow,
      auth,
      fieldPlacements,
      registerComponent,
      onValueChange,
      showInfoArea,
      entityCount,
      showEditBtn,
      editOn,
      eventBus,
      formatDate,
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
