<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Sets />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import { Sets } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "SetList",
  components: {
    SuspenseWithError,
    Sets,
  },
});
</script>
