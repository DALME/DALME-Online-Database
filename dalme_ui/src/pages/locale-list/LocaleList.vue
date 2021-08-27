<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Locales />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Locales } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "LocaleList",
  components: {
    SuspenseWithError,
    Locales,
  },
  setup() {
    useMeta({ title: "Locales" });
  },
});
</script>
