<template>
  <PageContainer>
    <CountryList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { CountryList, PageContainer } from "@/components";

export default defineComponent({
  name: "CountriesPageContainer",
  components: {
    CountryList,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Countries" });
  },
});
</script>
