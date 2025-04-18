<template>
  <PageContainer>
    <LocaleList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { LocaleList, PageContainer } from "@/components";

export default defineComponent({
  name: "LocalesPageContainer",
  components: {
    LocaleList,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Locales" });
  },
});
</script>
