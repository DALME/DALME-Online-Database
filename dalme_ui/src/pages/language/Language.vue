<template>
  <q-page> </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

// import { LanguageDetail } from "@/components";
// import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Language",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    // SuspenseWithError,
    // LanguageDetail,
  },
  setup(props) {
    useMeta({ title: `Language #${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
