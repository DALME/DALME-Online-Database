<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div v-if="showInfoArea && !loading" class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!loading">
                  {{ recordStore.current.name }}
                  <TagPill
                    v-if="recordStore.current.workflow.isPublic"
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
                    {{ formatDate(recordStore.current.creationTimestamp, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordStore.current.creationUser"
                    text-size="12px"
                    inline
                  />
                  <span
                    >, last modified on
                    {{ formatDate(recordStore.current.modificationTimestamp, "DATETIME_AT") }}
                    by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordStore.current.modificationUser"
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
            v-model="recordStore.tab"
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
                v-if="recordStore.current.pages.length > 0"
                class="side-tab"
                icon="o_import_contacts"
                label="Folios"
                name="pages"
              >
                <q-badge
                  :label="recordStore.current.pages.length"
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
                  v-if="recordStore.current.commentCount > 0"
                  :label="recordStore.current.commentCount"
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
                :value="recordStore.current.workflow.helpFlag"
                class="q-ml-xs"
                true-colour="red-4"
                true-icon="flag"
              />
            </div>
            <WorkflowManager
              v-if="auth.user.isSuperuser"
              @state-changed="updateWorkflow"
              :data="recordStore.current.workflow"
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
          <q-tab-panels v-model="recordStore.tab" animated keep-alive>
            <q-tab-panel class="q-pt-none q-px-none" name="info">
              <div class="col-9 q-pr-lg q-pt-md">
                <div class="row no-wrap">
                  <div class="col-6 q-mr-md">
                    <DetailCard
                      :width="cardWidth"
                      icon="bookmark"
                      title="Record"
                      pad-container-list
                    >
                      <InputField
                        :id="recordStore.current.id"
                        :repository="recordStore.Records"
                        field="name"
                        label="Name"
                      />
                      <InputField
                        :id="recordStore.current.id"
                        :repository="recordStore.Records"
                        field="shortName"
                        label="Short name"
                      />
                      <SelectField
                        :id="recordStore.current.id"
                        :repository="recordStore.Records"
                        field="ownerId"
                        label="Owner"
                      />
                    </DetailCard>
                    <MarkdownField
                      :id="recordStore.current.attributes.find((x) => x.name === 'description').id"
                      :repository="Attributes"
                      class="q-mt-md"
                      icon="subject"
                    />
                    <DetailCard
                      v-if="recordStore.current.pages.length > 0"
                      @value-changed="onValueChange"
                      class="q-mt-md"
                      icon="auto_stories"
                      title="Folios"
                      show-filter
                    >
                      <RecordPages :pages="recordStore.current.pages" />
                    </DetailCard>
                  </div>
                  <div class="col-6">
                    <AttributesCard
                      :id="recordStore.current.id"
                      :exclusions="['description']"
                      :repository="recordStore.Records"
                    />
                  </div>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel class="q-pt-sm q-px-none editor-panel" name="pages">
              <RecordEditor />
            </q-tab-panel>

            <q-tab-panel class="q-pt-none q-px-none" name="entities">
              <div class="col-9 q-pr-sm">
                <DetailCard
                  v-if="recordStore.current.agents.length > 0"
                  @value-changed="onValueChange"
                  class="q-mt-md"
                  icon="people"
                  title="Agents"
                  show-filter
                >
                  <RecordAgents :agents="recordStore.current.agents" />
                </DetailCard>

                <DetailCard
                  v-if="recordStore.current.places.length > 0"
                  @value-changed="onValueChange"
                  class="q-mt-md"
                  icon="mdi-map-marker"
                  title="Places"
                  show-filter
                >
                  <RecordPlaces :places="recordStore.current.places" />
                </DetailCard>
              </div>
            </q-tab-panel>

            <q-tab-panel class="q-pt-md q-px-lg" name="comments">
              <CommentBox
                @on-count-changed="updateCommentCount"
                :worklog="recordStore.current.workflow.workLog"
              />
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
      <div v-if="!loading && recordStore.tab !== 'pages'" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar :data="sidebarData">
          <template #extraElements>
            <SelectField
              :id="recordStore.current.id"
              :repository="recordStore.Records"
              chip-icon="mdi-folder-outline"
              field="collectionIds"
              label="Collections"
              multiple
              sidebar
            />
            <DetailElement v-if="recordStore.current.collections.length > 0" label="Collections">
              <template #content>
                <template
                  v-for="collection in recordStore.current.collections"
                  :key="collection.id"
                >
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
                    :user="recordStore.current.creationUser"
                    text-size="13px"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ formatDate(recordStore.current.creationTimestamp, "DATETIME_AT") }}
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
                    :user="recordStore.current.modificationUser"
                    text-size="13px"
                  />
                  <div class="text-detail text-grey-7 text-weight-medium">
                    {{ formatDate(recordStore.current.modificationTimestamp, "DATETIME_AT") }}
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
import { useMeta, useQuasar } from "quasar";
import { isEmpty, isNil, filter as rFilter } from "ramda";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import { requests } from "@/api";
import {
  AdaptiveSpinner,
  AttributesCard,
  BooleanValue,
  CommentBox,
  CustomDialog,
  DetailCard,
  DetailElement,
  DetailSidebar,
  RecordEditor,
  TagPill,
  UserPill,
  WorkflowManager,
} from "@/components";
import { InputField, MarkdownField, SelectField } from "@/components/fields";
import { Attributes } from "@/models";
import { attributeSchema, recordDetailSchema, workflowSchema } from "@/schemas";
import { useAPI, useEventHandling, useStores } from "@/use";
import { formatDate, getColumns, isObject, nully } from "@/utils";

import { metadata } from "./metadata";
import { columnMap } from "./pageColumns";
import RecordAgents from "./RecordAgents.vue";
import RecordPages from "./RecordPages.vue";
import RecordPlaces from "./RecordPlaces.vue";

export default defineComponent({
  name: "RecordDetail",
  components: {
    AttributesCard,
    AdaptiveSpinner,
    BooleanValue,
    CommentBox,
    DetailCard,
    DetailElement,
    DetailSidebar,
    RecordAgents,
    RecordEditor,
    MarkdownField,
    RecordPages,
    RecordPlaces,
    TagPill,
    UserPill,
    WorkflowManager,
    InputField,
    SelectField,
  },
  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const { eventBus, notifier } = useEventHandling();
    const { apiInterface } = useAPI();
    const { auth, ui, view, views, showEditBtn, showInfoArea, editOn, recordStore } = useStores();
    const { success, data, fetchAPI } = apiInterface();
    const id = ref($route.params.id);
    const pageColumns = ref(getColumns(columnMap));
    const refRegister = ref({});
    const loading = ref(true);

    const cardWidth = computed(() => {
      return "200";
    });

    const sidebarData = computed(() =>
      addMetadata([
        ["id", recordStore.current.id],
        ["mk1Identifier", recordStore.current.attr("mk1Identifier")],
        ["mk2Identifier", recordStore.current.attr("mk2Identifier")],
        ["altIdentifier", recordStore.current.attr("altIdentifier")],
      ]),
    );

    const infoCardData = computed(() =>
      addMetadata([
        ["name", recordStore.current.name],
        ["shortName", recordStore.current.shortName],
        ["recordType", recordStore.current.attr("recordType")],
        ["hasInventory", recordStore.current.attr("hasInventory")],
        ["parent", recordStore.current.parent],
        ["owner", recordStore.current.owner],
        ["date", recordStore.current.attr("date")],
        ["startDate", recordStore.current.attr("startDate")],
        ["endDate", recordStore.current.attr("endDate")],
        ["language", recordStore.current.attr("language")],
        ["locale", recordStore.current.attr("locale")],
        ["debtPhrase", recordStore.current.attr("debtPhrase")],
        ["debtAmount", recordStore.current.attr("debtAmount")],
        ["debtUnit", recordStore.current.attr("debtUnit")],
        ["debtUnitSource", recordStore.current.attr("debtUnitSource")],
        ["debtSource", recordStore.current.attr("debtSource")],
      ]),
    );

    const descriptionData = computed(() =>
      addMetadata([["description", recordStore.current.attr("description")]]),
    );

    const addMetadata = (fields) =>
      rFilter((x) => !isNil(x[1]) && !isEmpty(x[1]), fields).map(([k, v], i) =>
        isObject(v)
          ? Object.assign({ field: k, order: i }, metadata[k], v)
          : Object.assign({ field: k, value: v, order: i }, metadata[k]),
      );

    const entityCount = computed(
      () => recordStore.current.agents.length + recordStore.current.places.length,
    );

    useMeta(() => ({
      title: !nully(view.value.recordData)
        ? view.value.recordData.name.value
        : `Record ${id.value}`,
    }));

    const updateCommentCount = (cnt) => {
      view.value.commentCount = cnt;
    };

    const registerComponent = (name, reference) => {
      console.log("Register component", name, reference);
      if (reference) {
        refRegister.value[name] = reference;
      }
    };

    const updateWorkflow = async (newState) => {
      await fetchAPI(requests.workflow.changeState(id.value, newState));
      if (success.value) {
        await workflowSchema.validate(data.value, { stripUnknown: false }).then((value) => {
          view.value.workflowData = value;
        });
      } else {
        notifier.workflow.updateFailed();
      }
    };

    const editHandlers = (payload) => {
      if (payload.source === "attribute") {
        const request = payload.update
          ? requests.attributes.updateValue(payload.id, payload.value)
          : requests.records.addAttribute(id.value, snakeCase(payload.name), payload.value);
        const notifier = (name) =>
          payload.update
            ? notifier.attributes.updateFailed(name)
            : notifier.records.addAttributeFailed(name);
        const handler = (name, value, _restore) =>
          (view.value.recordData[name] = Object.assign(view.value.recordData[name], value));
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
          (view.value.recordData[name].value = _restore ? value : value[name]);
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
        console.log("RECORD DETAIL WATCHER");
        if (to) {
          loading.value = true;
          ui.resetBreadcrumbTail();
          await recordStore.setCurrent(to);
          id.value = recordStore.current.id;
          ui.breadcrumbTail.push(recordStore.current.shortName);
          loading.value = false;
          window.testRS = recordStore;
        }
      },
      { immediate: true, flush: "post" },
    );

    provide("model", "Record");
    provide("id", id);
    provide("pageColumns", pageColumns);

    onBeforeRouteLeave(() => {
      if (views.hasChanges) {
        return new Promise((resolve) => {
          $q.dialog({
            component: CustomDialog,
            componentProps: {
              isPersistent: true,
              title: "Unsaved changes",
              closeIcon: false,
              message:
                "<b>Are you sure you wish to leave?</b>\
                There are unsaved changes in the current record.",
              icon: "mdi-alert-outline",
              okayButtonLabel: "Leave",
            },
          })
            .onOk(() => {
              return resolve(true);
            })
            .onCancel(() => {
              return resolve(false);
            });
        });
      }
    });

    return {
      updateCommentCount,
      view,
      ui,
      updateWorkflow,
      auth,
      registerComponent,
      onValueChange,
      showInfoArea,
      entityCount,
      showEditBtn,
      editOn,
      eventBus,
      formatDate,
      loading,
      recordStore,
      sidebarData,
      infoCardData,
      descriptionData,
      cardWidth,
      Attributes,
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
