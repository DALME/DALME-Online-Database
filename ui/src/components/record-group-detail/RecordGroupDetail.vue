<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div class="info-area row" v-if="!ui.globalLoading">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!ui.globalLoading">
                  {{ recordGroup.name }}
                </template>
                <q-skeleton v-else width="350px" height="30px" type="rect" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!ui.globalLoading">
                  <span
                    >Created on {{ recordGroup.creationTimestamp.date }} @
                    {{ recordGroup.creationTimestamp.time }} by
                  </span>
                  <UserPill
                    :user="recordGroup.creationUser"
                    text-size="12px"
                    :show-avatar="false"
                    inline
                  />
                  <span
                    >, last modified on {{ recordGroup.modificationTimestamp.date }} @
                    {{ recordGroup.modificationTimestamp.time }} by
                  </span>
                  <UserPill
                    :user="recordGroup.modificationUser"
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
                          class="text-link"
                          :to="{
                            name: 'User',
                            params: { username: recordGroup.owner.username },
                          }"
                        >
                          {{ recordGroup.owner.fullName }}
                        </router-link>
                        <q-chip
                          v-if="recordGroup.isPrivate"
                          dense
                          size="10px"
                          outline
                          color="red-10"
                          class="q-ml-sm text-bold"
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
                    icon="subject"
                    title="Description"
                    noData="No description assigned."
                    pad-container
                    class="q-mt-md"
                  >
                    <MarkdownEditor
                      v-if="recordGroup.description"
                      :text="recordGroup.description"
                    />
                  </DetailCard>
                  <DetailCard
                    v-if="!nully(recordGroup.children)"
                    icon="account_tree"
                    title="Children"
                    showFilter
                    class="q-mt-md"
                  >
                    <RecordChildren overview :children="recordGroup.children" />
                  </DetailCard>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel name="comments" class="q-pt-md q-px-lg">
              <CommentBox @on-count-changed="updateCommentCount" />
            </q-tab-panel>
          </q-tab-panels>
        </template>
        <AdaptiveSpinner v-else />
      </div>
      <div v-if="!ui.globalLoading" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar>
          <template v-slot:extraElements>
            <DetailElement label="Unique Id" clipboard :content="recordGroup.id" />
            <DetailElement label="Created">
              <template v-slot:content>
                <div>
                  <UserPill :user="recordGroup.creationUser" text-size="13px" :bold="false" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ recordGroup.creationTimestamp.date }} @
                    {{ recordGroup.modificationTimestamp.time }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template v-slot:content>
                <div>
                  <UserPill :user="recordGroup.modificationUser" text-size="13px" :bold="false" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ recordGroup.modificationTimestamp.date }} @
                    {{ recordGroup.modificationTimestamp.time }}
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
import { useAPI, useEditing, useStores } from "@/use";
import RecordChildren from "./RecordChildren.vue";
import { nully } from "@/utils";
import {
  AdaptiveSpinner,
  CommentBox,
  DetailCard,
  DetailSidebar,
  DetailElement,
  MarkdownEditor,
  UserPill,
} from "@/components";
import { recordGroupSchema } from "@/schemas";

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
    const { editingDetailRouteGuard, resource } = useEditing();
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
          resource.value = "recordGroup";
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

    editingDetailRouteGuard();

    return {
      commentCount,
      updateCommentCount,
      view,
      resource,
      recordGroup,
      ui,
      isAdmin: auth.user.isAdmin,
      nully,
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
