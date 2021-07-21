<template>
  <q-page> </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

// import { LocaleDetail } from "@/components";
// import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Locale",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    // SuspenseWithError,
    // LocaleDetail,
  },
  setup(props) {
    useMeta({ title: `Locale #${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
