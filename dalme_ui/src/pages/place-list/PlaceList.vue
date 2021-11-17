<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <Places />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Places } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "PlaceList",
  components: {
    SuspenseWithError,
    Page,
    Places,
  },
  setup() {
    useMeta({ title: "Places" });
  },
});
</script>
