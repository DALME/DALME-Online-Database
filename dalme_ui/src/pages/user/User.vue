<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <UserDetail />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { defineComponent } from "vue";

import { Page, UserDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "User",
  components: {
    Page,
    SuspenseWithError,
    UserDetail,
  },
});
</script>
