<template>
  <Page>
    <div class="full-width full-height">
      <SetDetail />
      <Comments />
    </div>
  </Page>
</template>

<script>
import { computed, defineComponent, provide } from "vue";
import { useRoute } from "vue-router";

import { Comments, Page, SetDetail } from "@/components";

export default defineComponent({
  name: "Set",
  components: {
    Comments,
    Page,
    SetDetail,
  },
  setup() {
    const $route = useRoute();

    const id = computed(() => $route.params.id);

    provide("model", "Set");
    provide("id", id);
  },
});
</script>
