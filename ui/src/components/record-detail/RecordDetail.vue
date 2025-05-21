<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div v-if="showInfoArea && !loading" class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!loading">
                  {{ Records.current.name }}
                  <TagPill
                    v-if="Records.current.workflow.isPublic"
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
                    {{ formatDate(Records.current.creationTimestamp, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="Records.current.creationUser"
                    text-size="12px"
                    inline
                  />
                  <span
                    >, last modified on
                    {{ formatDate(Records.current.modificationTimestamp, "DATETIME_AT") }}
                    by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="Records.current.modificationUser"
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
            v-model="Records.tab"
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
                v-if="Records.pageCount > 0"
                class="side-tab"
                icon="o_import_contacts"
                label="Folios"
                name="pages"
              >
                <q-badge
                  :label="Records.pageCount"
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
                  v-if="Records.current.commentCount > 0"
                  :label="Records.current.commentCount"
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
                :value="Records.current.workflow.helpFlag"
                class="q-ml-xs"
                true-colour="red-4"
                true-icon="flag"
              />
            </div>
            <WorkflowManager v-if="auth.user.isSuperuser" :data="Records.current.workflow" />
            <q-btn
              v-if="Records.showEditBtn"
              @click="eventBus.emit('toggleEditor')"
              :icon="Records.editOn ? 'mdi-pencil-off' : 'mdi-pencil'"
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
          <q-tab-panels v-model="Records.tab" animated keep-alive>
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
                        :id="Records.current.id"
                        :repository="Records"
                        field="name"
                        label="Name"
                      />
                      <InputField
                        :id="Records.current.id"
                        :repository="Records"
                        field="shortName"
                        label="Short name"
                      />
                      <SelectField
                        :id="Records.current.id"
                        :repository="Records"
                        field="ownerId"
                        label="Owner"
                      />
                    </DetailCard>
                    <MarkdownField
                      :id="descriptionId"
                      :creating="descriptionId ? false : true"
                      :repository="Attributes"
                      class="q-mt-md"
                      icon="subject"
                      label="Description"
                      placeholder="This record has no description."
                    />
                    <DetailCard
                      v-if="Records.pageCount > 0"
                      class="q-mt-md"
                      icon="auto_stories"
                      title="Folios"
                      show-filter
                    >
                      <RecordPages :pages="Records.current.pages" />
                    </DetailCard>
                  </div>
                  <div class="col-6">
                    <AttributesCard
                      :id="Records.current.id"
                      :exclusions="['description']"
                      :order="attributesOrder"
                      :repository="Records"
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
                  v-if="Records.current.agents.length > 0"
                  class="q-mt-md"
                  icon="people"
                  title="Agents"
                  show-filter
                >
                  <RecordAgents :agents="Records.current.agents" />
                </DetailCard>

                <DetailCard
                  v-if="locations.length > 0"
                  class="q-mt-md"
                  icon="mdi-map-marker"
                  title="Locations"
                  show-filter
                >
                  <RecordLocations :targets="locations" />
                </DetailCard>
              </div>
            </q-tab-panel>

            <q-tab-panel class="q-pt-md q-px-lg" name="comments">
              <CommentBox
                @on-count-changed="updateCommentCount"
                :worklog="Records.current.workflow.workLog"
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
      <div v-if="!loading && Records.tab !== 'pages'" class="col-3 q-pl-md q-pt-md">
        <SidebarItem :content="Records.current.id" label="Unique Id" clipboard />
        <SelectField
          :id="Records.current.id"
          :repository="Records"
          chip-icon="mdi-folder-outline"
          field="collectionIds"
          label="Collections"
          placeholder="Not included in any collection."
          multiple
          sidebar
        />
        <SidebarItem label="Created">
          <template #content>
            <div>
              <UserPill
                :bold="false"
                :show-avatar="false"
                :user="Records.current.creationUser"
                text-size="13px"
              />
              <div class="text-detail text-grey-7 text-weight-medium">
                {{ formatDate(Records.current.creationTimestamp, "DATETIME_AT") }}
              </div>
            </div>
          </template>
        </SidebarItem>
        <SidebarItem label="Last modified">
          <template #content>
            <div>
              <UserPill
                :bold="false"
                :show-avatar="false"
                :user="Records.current.modificationUser"
                text-size="13px"
              />
              <div class="text-detail text-grey-7 text-weight-medium">
                {{ formatDate(Records.current.modificationTimestamp, "DATETIME_AT") }}
              </div>
            </div>
          </template>
        </SidebarItem>
      </div>
    </div>
  </div>
</template>

<script>
import { useMeta, useQuasar } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";

import {
  AdaptiveSpinner,
  AttributesCard,
  BooleanValue,
  CommentBox,
  CustomDialog,
  DetailCard,
  RecordEditor,
  SidebarItem,
  TagPill,
  UserPill,
  WorkflowManager,
} from "@/components";
import { InputField, MarkdownField, SelectField } from "@/components/fields";
import { Attributes, Records } from "@/models";
import { useEventHandling, useStores } from "@/use";
import { formatDate, getColumns, nully } from "@/utils";

import { columnMap } from "./pageColumns";
import RecordAgents from "./RecordAgents.vue";
import RecordLocations from "./RecordLocations.vue";
import RecordPages from "./RecordPages.vue";

export default defineComponent({
  name: "RecordDetail",
  components: {
    AttributesCard,
    AdaptiveSpinner,
    BooleanValue,
    CommentBox,
    DetailCard,
    RecordAgents,
    RecordEditor,
    MarkdownField,
    RecordPages,
    RecordLocations,
    TagPill,
    UserPill,
    WorkflowManager,
    InputField,
    SelectField,
    SidebarItem,
  },
  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const { eventBus } = useEventHandling();
    const { auth, ui, showInfoArea } = useStores();
    const id = ref($route.params.id);
    const pageColumns = ref(getColumns(columnMap));
    const loading = ref(true);

    const cardWidth = computed(() => {
      return "200";
    });

    const descriptionId = computed(() => {
      const descAttr = Records.current.attributes.find((x) => x.name === "description");
      return descAttr ? descAttr.id : null;
    });

    const locations = computed(() => {
      const locales = Records.current.attributes.filter((x) => x.name === "locale");
      const places = Records.current.places;
      let locs = [];
      console.log("locale attr", locales, places);
      if (locales.length > 0) locs = locs.concat(locales);
      if (places.length > 0) locs = locs.concat(places);
      return locs.length > 0 ? locs : null;
    });

    const attributesOrder = [
      "recordType",
      "hasInventory",
      "mk1Identifier",
      "mk2Identifier",
      "altIdentifier",
      "date",
      "startDate",
      "endDate",
      "language",
      "locale",
      "debtPhrase",
      "debtAmount",
      "debtUnit",
      "debtUnitSource",
      "debtSource",
    ];

    const entityCount = computed(
      () => Records.current.agents.length + Records.current.places.length,
    );

    useMeta(() => ({
      title: !nully(Records.current) ? Records.current.name : `Record ${id.value}`,
    }));

    const updateCommentCount = (cnt) => {
      Records.current.commentCount = cnt;
    };

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          loading.value = true;
          ui.resetBreadcrumbTail();
          await Records.setCurrent(to);
          id.value = Records.current.id;
          ui.breadcrumbTail.push(Records.current.shortName);
          loading.value = false;
        }
      },
      { immediate: true, flush: "post" },
    );

    provide("model", "Record");
    provide("id", id);
    provide("pageColumns", pageColumns);

    onBeforeRouteLeave(() => {
      if (Records.hasChanges) {
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
      Attributes,
      attributesOrder,
      auth,
      cardWidth,
      descriptionId,
      entityCount,
      eventBus,
      formatDate,
      loading,
      locations,
      Records,
      showInfoArea,
      ui,
      updateCommentCount,
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
