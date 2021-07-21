<template>
  <q-page> </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

// import { RightsDetail } from "@/components";
// import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Rights",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    // SuspenseWithError,
    // RightsDetail,
  },
  setup(props) {
    // TODO: We want to use the name here...
    useMeta({ title: `Rights ${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
