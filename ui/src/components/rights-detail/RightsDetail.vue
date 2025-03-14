<template>
  <div class="full-width full-height">
    <div class="row">
      <div class="col-grow">
        <transition name="collapse">
          <div class="info-area row" v-if="!loading">
            <div class="column">
              <div class="row items-center text-h5">
                <template v-if="!loading">
                  {{ policy.name }}
                  <TagPill
                    :name="policy.rightsStatus.name"
                    :colour="statusColours.colour"
                    :textColour="statusColours.text"
                    size="sm"
                    module="standalone"
                    class="q-ml-md q-mt-xs"
                  />
                </template>
                <q-skeleton v-else width="350px" height="30px" type="rect" />
              </div>
              <div class="row detail-row-subheading text-grey-8">
                <template v-if="!loading">
                  <span
                    >Created on {{ policy.creationTimestamp.date }} @
                    {{ policy.creationTimestamp.time }} by
                  </span>
                  <UserPill
                    :user="policy.creationUser"
                    text-size="12px"
                    :show-avatar="false"
                    inline
                  />
                  <span
                    >, last modified on {{ policy.modificationTimestamp.date }} @
                    {{ policy.modificationTimestamp.time }} by
                  </span>
                  <UserPill
                    :user="policy.modificationUser"
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
            <template v-if="!loading">
              <q-tab name="comments" icon="o_forum" label="Discussion">
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
      <div class="col-9 q-pr-md">
        <template v-if="!loading">
          <q-tab-panels
            v-model="view.tab"
            animated
            transition-prev="jump-up"
            transition-next="jump-up"
            keep-alive
          >
            <q-tab-panel name="info" class="q-pt-none q-px-none">
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
                    icon="preview"
                    title="Attachment preview"
                    class="q-mt-md"
                    pad-container
                  >
                    <div class="row q-mt-xs">
                      <embed
                        src="/media/dalme/attachments/2020/12/
AD_Savoie_-_Autorisation_de_publication.pdf"
                        type="application/pdf"
                        class="embeddedDocPdf"
                        height="700px"
                      />
                    </div>
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
      <div v-if="!loading" class="col-3 q-pl-md q-pt-md">
        <DetailSidebar>
          <template v-slot:extraElements>
            <DetailElement label="Attachment">
              <template v-slot:content>
                <template v-if="policy.attachments">
                  <AttachmentWidget :file="policy.attachments" color="indigo-6" compact />
                </template>
                <div class="text-13" v-else>None yet</div>
              </template>
            </DetailElement>
            <DetailElement label="Unique Id" clipboard :content="policy.id" />
            <DetailElement label="Created">
              <template v-slot:content>
                <div>
                  <UserPill :user="policy.creationUser" text-size="13px" :bold="false" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ policy.creationTimestamp.date }} @
                    {{ policy.modificationTimestamp.time }}
                  </div>
                </div>
              </template>
            </DetailElement>
            <DetailElement label="Last modified">
              <template v-slot:content>
                <div>
                  <UserPill :user="policy.modificationUser" text-size="13px" :bold="false" />
                  <div class="text-detail text-grey-7 text-weight-medium q-pl-lg">
                    {{ policy.modificationTimestamp.date }} @
                    {{ policy.modificationTimestamp.time }}
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
import { computed, defineComponent, ref, readonly, provide, watch } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { useAPI, useStores, useConstants } from "@/use";
import { rightsSchema } from "@/schemas";
import {
  AdaptiveSpinner,
  AttachmentWidget,
  BooleanValue,
  CommentBox,
  DetailCard,
  DetailSidebar,
  DetailElement,
  TagPill,
  UserPill,
} from "@/components";

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

<style lang="scss">
.embeddedDocPdf {
  width: 100%;
}
</style>
