<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div v-if="!ui.globalLoading" class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!ui.globalLoading">
                  {{ recordGroup.name }}
                </template>
                <q-skeleton v-else height="30px" type="rect" width="350px" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!ui.globalLoading">
                  <span
                    >Created on
                    {{ formatDate(recordGroup.creationTimestamp.value, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordGroup.creationUser"
                    text-size="12px"
                    inline
                  />
                  <span
                    >, last modified on
                    {{ formatDate(recordGroup.modificationTimestamp.value, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="recordGroup.modificationUser"
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
            <template v-if="!ui.globalLoading">
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
            <AdaptiveSpinner v-else class="q-ml-md" size="sm" type="bars" />
          </q-tabs>
        </div>
      </div>
    </div>
    <div class="row q-pt-sm">
      <div class="col">
        <template v-if="!ui.globalLoading">
          <q-tab-panels v-model="view.tab" animated keep-alive>
            <q-tab-panel class="q-pt-none q-px-none" name="info">
              <div class="row q-pt-md">
                <div class="col q-pr-md">
                  <DetailCard icon="bookmark" title="Record" pad-container>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Name</div>
                      <div class="col-8">{{ recordGroup.name }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Short name</div>
                      <div class="col-8">{{ recordGroup.shortName }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Owner</div>
                      <div class="col-8">
                        <router-link
                          :to="{
                            name: 'User',
                            params: { username: recordGroup.owner.username },
                          }"
                          class="text-link"
                        >
                          {{ recordGroup.owner.fullName }}
                        </router-link>
                        <q-chip
                          v-if="recordGroup.isPrivate"
                          class="q-ml-sm text-bold"
                          color="red-10"
                          size="10px"
                          dense
                          outline
                        >
                          PRIVATE
                        </q-chip>
                      </div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Authority</div>
                      <div class="col-8">{{ recordGroup.authority }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Format</div>
                      <div class="col-8">{{ recordGroup.format }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Support</div>
                      <div class="col-8">{{ recordGroup.support }}</div>
                    </div>
                  </DetailCard>
                  <DetailCard
                    class="q-mt-md"
                    icon="subject"
                    no-data="No description assigned."
                    title="Description"
                    pad-container
                  >
                    <MarkdownEditor
                      v-if="recordGroup.description"
                      :text="recordGroup.description"
                    />
                  </DetailCard>
                  <DetailCard
                    v-if="!nully(recordGroup.children)"
                    class="q-mt-md"
                    icon="account_tree"
                    title="Children"
                    show-filter
                  >
                    <RecordChildren :children="recordGroup.children" overview />
                  </DetailCard>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel class="q-pt-md q-px-lg" name="comments">
              <CommentBox @on-count-changed="updateCommentCount" />
            </q-tab-panel>
          </q-tab-panels>
        </template>
        <AdaptiveSpinner v-else />
      </div>
      <div v-if="!ui.globalLoading" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar>
          <template #extraElements>
            <DetailElement :content="recordGroup.id" label="Unique Id" clipboard />
            <DetailElement label="Created">
              <template #content>
                <div>
                  <UserPill :bold="false" :user="recordGroup.creationUser" text-size="13px" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ formatDate(recordGroup.creationTimestamp.value, "DATETIME_AT") }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template #content>
                <div>
                  <UserPill :bold="false" :user="recordGroup.modificationUser" text-size="13px" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ formatDate(recordGroup.modificationTimestamp.value, "DATETIME_AT") }}
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
import {
  AdaptiveSpinner,
  CommentBox,
  DetailCard,
  DetailElement,
  DetailSidebar,
  MarkdownEditor,
  UserPill,
} from "@/components";
import { recordGroupSchema } from "@/schemas";
import { useAPI, useStores } from "@/use";
import { nully } from "@/utils";

import RecordChildren from "./RecordChildren.vue";

export default defineComponent({
  name: "RecordGroupDetail",
  components: {
    AdaptiveSpinner,
    CommentBox,
    DetailCard,
    DetailSidebar,
    DetailElement,
    MarkdownEditor,
    UserPill,
    RecordChildren,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { auth, ui, view } = useStores();
    const { success, data, fetchAPI } = apiInterface();
    const recordGroup = ref({});
    const id = ref($route.params.id);
    const commentCount = ref(0);

    provide("model", "RecordGroup");
    provide("id", id);

    useMeta(() => ({
      title: recordGroup.value ? recordGroup.value.shortName : `Record Group ${id.value}`,
    }));

    const fetchData = async () => {
      ui.globalLoading = true;
      await fetchAPI(requests.recordGroups.getRecordGroup(id.value));
      if (success.value) {
        await recordGroupSchema.validate(data.value, { stripUnknown: false }).then((value) => {
          recordGroup.value = value;
          commentCount.value = value.commentCount;
          ui.breadcrumbTail.push(value.shortName);
          ui.globalLoading = false;
        });
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

    return {
      commentCount,
      updateCommentCount,
      view,
      recordGroup,
      ui,
      isAdmin: auth.user.isAdmin,
      nully,
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
