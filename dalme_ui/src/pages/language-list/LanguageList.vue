<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Languages />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Languages } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "LanguageList",
  components: {
    SuspenseWithError,
    Languages,
  },
  setup() {
    useMeta({ title: "Languages" });
  },
});
</script>
