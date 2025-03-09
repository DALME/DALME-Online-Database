<template>
  <PageContainer>
    <LanguageList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { LanguageList, PageContainer } from "@/components";

export default defineComponent({
  name: "LanguagesPageContainer",
  components: {
    LanguageList,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Languages" });
  },
});
</script>
