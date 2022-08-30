<template>
  <Page>
    <div class="full-width full-height"><SourceDetail /></div>
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
    const showModal = ref(false);

    provide("model", "Source");
    provide("id", id);

    return {
      showModal,
    };
  },
});
</script>
