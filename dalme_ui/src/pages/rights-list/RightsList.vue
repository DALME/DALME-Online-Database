<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <Rights />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Rights } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "RightsList",
  components: {
    Page,
    SuspenseWithError,
    Rights,
  },
  setup() {
    useMeta({ title: "Issue Rights" });
  },
});
</script>
