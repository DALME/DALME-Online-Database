<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Rights />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Rights } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "RightsList",
  components: {
    SuspenseWithError,
    Rights,
  },
  setup() {
    useMeta({ title: "Issue Rights" });
  },
});
</script>
