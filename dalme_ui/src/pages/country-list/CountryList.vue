<template>
  <q-page>
    <Countries />
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Countries } from "@/components";

export default defineComponent({
  name: "CountryList",
  components: {
    Countries,
  },
  setup() {
    useMeta({ title: "Countries" });
  },
});
</script>
