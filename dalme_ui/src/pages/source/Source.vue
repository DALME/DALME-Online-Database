<template>
  <Page>
    <div class="full-width full-height">
      <q-splitter :horizontal="$q.screen.lt.sm" v-model="splitterModel">
        <template v-slot:before>
          <q-tabs v-model="tab" class="text-blue" :vertical="$q.screen.gt.xs">
            <q-tab name="data" icon="info" label="Data" />
            <q-tab v-if="hasPages" name="pages" icon="preview" label="Pages" />
          </q-tabs>
        </template>

        <template v-slot:after>
          <q-tab-panels
            v-model="tab"
            animated
            swipeable
            transition-prev="jump-up"
            transition-next="jump-up"
          >
            <q-tab-panel name="data">
              <SourceDetail />
            </q-tab-panel>
          </q-tab-panels>

          <Comments />
        </template>
      </q-splitter>
    </div>
  </Page>
</template>

<script>
import { computed, defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { Comments, Page, SourceDetail } from "@/components";

export default defineComponent({
  name: "Source",
  components: {
    Comments,
    Page,
    SourceDetail,
  },
  setup() {
    const $route = useRoute();

    const id = computed(() => $route.params.id);
    const hasPages = ref(null);
    const tab = ref("data");
    const splitterModel = ref(10);

    provide("model", "Source");
    provide("id", id);
    provide("hasPages", hasPages);

    const showModal = ref(false);

    return { hasPages, showModal, splitterModel, tab };
  },
});
</script>
