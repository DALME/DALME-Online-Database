<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <SetDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { SetDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Set",
  components: {
    SuspenseWithError,
    SetDetail,
  },
});
</script>
