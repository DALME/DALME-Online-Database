<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Places />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Places } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "PlaceList",
  components: {
    SuspenseWithError,
    Places,
  },
  setup() {
    useMeta({ title: "Places" });
  },
});
</script>
