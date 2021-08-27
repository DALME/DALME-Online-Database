<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Countries />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Countries } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "CountryList",
  components: {
    SuspenseWithError,
    Countries,
  },
  setup() {
    useMeta({ title: "Countries" });
  },
});
</script>
