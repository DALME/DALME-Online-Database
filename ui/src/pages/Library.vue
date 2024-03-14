<template>
  <PageContainer>
    <LibraryList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { LibraryList, PageContainer } from "@/components";

export default defineComponent({
  name: "LibraryPageContainer",
  components: {
    LibraryList,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Library" });
  },
});
</script>
