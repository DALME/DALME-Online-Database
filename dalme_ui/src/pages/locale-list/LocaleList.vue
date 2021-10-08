<template>
  <q-page>
    <Locales />
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Locales } from "@/components";

export default defineComponent({
  name: "LocaleList",
  components: {
    Locales,
  },
  setup() {
    useMeta({ title: "Locales" });
  },
});
</script>
