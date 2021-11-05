<template>
  <q-page>
    <Languages />
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Languages } from "@/components";

export default defineComponent({
  name: "LanguageList",
  components: {
    Languages,
  },
  setup() {
    useMeta({ title: "Languages" });
  },
});
</script>
