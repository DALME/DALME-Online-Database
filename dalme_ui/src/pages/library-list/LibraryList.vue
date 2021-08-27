<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Library />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Library } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "LibraryList",
  components: {
    SuspenseWithError,
    Library,
  },
  setup() {
    useMeta({ title: "Library" });
  },
});
</script>
