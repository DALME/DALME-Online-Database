<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <Library />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Library, Page } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "LibraryList",
  components: {
    SuspenseWithError,
    Library,
    Page,
  },
  setup() {
    useMeta({ title: "Library" });
  },
});
</script>
