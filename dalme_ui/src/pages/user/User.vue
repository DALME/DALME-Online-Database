<template>
  <Page>
    <UserDetail />
  </Page>
</template>

<script>
import { defineComponent } from "vue";

import { Page, UserDetail } from "@/components";

export default defineComponent({
  name: "User",
  components: {
    Page,
    UserDetail,
  },
});
</script>
