<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div v-if="!loading" class="info-area row">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!loading">
                  {{ policy.name }}
                  <TagPill
                    :colour="statusColours.colour"
                    :name="policy.rightsStatus.name"
                    :text-colour="statusColours.text"
                    class="q-ml-md q-mt-xs"
                    module="standalone"
                    size="sm"
                  />
                </template>
                <q-skeleton v-else height="30px" type="rect" width="350px" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!loading">
                  <span
                    >Created on {{ formatDate(policy.creationTimestamp.value, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="policy.creationUser"
                    text-size="12px"
                    inline
                  />
                  <span
                    >, last modified on
                    {{ formatDate(policy.modificationTimestamp.value, "DATETIME_AT") }} by
                  </span>
                  <UserPill
                    :show-avatar="false"
                    :user="policy.modificationUser"
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
              <q-tab icon="o_forum" label="Discussion" name="comments">
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
      <div class="col-9 q-pr-md">
        <template v-if="!loading">
          <q-tab-panels v-model="view.tab" animated keep-alive>
            <q-tab-panel class="q-pt-none q-px-none" name="info">
              <div v-if="policy" class="row q-pt-md">
                <div class="col">
                  <DetailCard icon="bookmark" title="Record" pad-container>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Name</div>
                      <div class="col-8">{{ policy.name }}</div>
                    </div>
                    <div v-if="policy.licence" class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Licence</div>
                      <div class="col-8">{{ policy.licence }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Public display</div>
                      <div class="col-8"><BooleanValue :value="policy.publicDisplay" /></div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Rights</div>
                      <div class="col-8">{{ policy.rights }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Rights holder</div>
                      <div class="col-8">{{ policy.rightsHolder }}</div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Notice display</div>
                      <div class="col-8"><BooleanValue :value="policy.noticeDisplay" /></div>
                    </div>
                    <div class="row q-mt-xs">
                      <div class="col-3 text-weight-medium text-right q-mr-lg">Notice</div>
                      <div class="col-8">{{ policy.rightsNotice }}</div>
                    </div>
                  </DetailCard>
                  <DetailCard
                    v-if="policy.attachments"
                    class="q-mt-md"
                    icon="preview"
                    title="Attachment preview"
                    pad-container
                  >
                    <div class="row q-mt-xs">
                      <embed
                        class="embeddedDocPdf"
                        height="700px"
                        src="/media/dalme/attachments/2020/12/
AD_Savoie_-_Autorisation_de_publication.pdf"
                        type="application/pdf"
                      />
                    </div>
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
      <div v-if="!loading" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar>
          <template #extraElements>
            <DetailElement label="Attachment">
              <template #content>
                <template v-if="policy.attachments">
                  <AttachmentWidget :file="policy.attachments" color="indigo-6" compact />
                </template>
                <div v-else class="text-13">None yet</div>
              </template>
            </DetailElement>
            <DetailElement :content="policy.id" label="Unique Id" clipboard />
            <DetailElement label="Created">
              <template #content>
                <div>
                  <UserPill :bold="false" :user="policy.creationUser" text-size="13px" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ formatDate(policy.creationTimestamp.value, "DATETIME_AT") }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template #content>
                <div>
                  <UserPill :bold="false" :user="policy.modificationUser" text-size="13px" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ formatDate(policy.modificationTimestamp.value, "DATETIME_AT") }}
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
import { computed, defineComponent, provide, readonly, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import {
  AdaptiveSpinner,
  AttachmentWidget,
  BooleanValue,
  CommentBox,
  DetailCard,
  DetailElement,
  DetailSidebar,
  TagPill,
  UserPill,
} from "@/components";
import { rightsSchema } from "@/schemas";
import { useAPI, useConstants, useStores } from "@/use";

export default defineComponent({
  name: "RightsDetail",
  components: {
    AdaptiveSpinner,
    AttachmentWidget,
    BooleanValue,
    CommentBox,
    DetailCard,
    DetailSidebar,
    DetailElement,
    TagPill,
    UserPill,
  },
  setup() {
    const $route = useRoute();
    const { auth, ui, view } = useStores();
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const { rightsColoursById } = useConstants();
    const model = "RightsPolicy";
    const id = computed(() => $route.params.id);
    const policy = ref({});
    const commentCount = ref(0);
    const loading = ref(true);

    useMeta(() => ({
      title: policy.value ? policy.value.name : `Policy ${id.value}`,
    }));

    const statusColours = computed(() => rightsColoursById[policy.value.rightsStatus.id]);

    provide("model", model);
    provide("id", readonly(id));

    const fetchData = async () => {
      await fetchAPI(requests.rights.getPolicy(id.value));
      if (success.value)
        await rightsSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          policy.value = value;
          commentCount.value = value.commentCount;
          ui.breadcrumbTail.push(value.name);
          loading.value = false;
        });
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
      policy,
      isAdmin: auth.user.isAdmin,
      loading,
      view,
      updateCommentCount,
      commentCount,
      statusColours,
    };
  },
});
</script>

<style lang="scss" scoped>
.embeddedDocPdf {
  width: 100%;
}
</style>
