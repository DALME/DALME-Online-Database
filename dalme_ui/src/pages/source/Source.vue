<template>
  <Page>
    <div class="full-width full-height q-px-content-visual">
      <SourceDetail />
    </div>
  </Page>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";
import { Page, SourceDetail } from "@/components";

export default defineComponent({
  name: "Source",
  components: {
    Page,
    SourceDetail,
  },
  setup() {
    const $route = useRoute();
    const id = ref($route.params.id);

    provide("model", "Source");
    provide("id", id);
  },
});
</script>
