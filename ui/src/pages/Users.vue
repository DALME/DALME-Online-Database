<template>
  <PageContainer>
    <div class="data-view">
      <router-view />
    </div>
  </PageContainer>
</template>

<script>
import { defineComponent } from "vue";

import { PageContainer } from "@/components";

export default defineComponent({
  name: "UsersPageContainer",
  components: { PageContainer },
});
</script>
