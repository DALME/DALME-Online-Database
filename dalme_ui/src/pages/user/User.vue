<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <UserDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { UserDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "User",
  components: {
    SuspenseWithError,
    UserDetail,
  },
});
</script>
