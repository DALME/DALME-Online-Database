<template>
  <PageContainer>
    <router-view />
  </PageContainer>
</template>

<script>
import { defineComponent } from "vue";

import { PageContainer } from "@/components";

export default defineComponent({
  name: "RecordGroupsPageContainer",
  components: { PageContainer },
});
</script>
