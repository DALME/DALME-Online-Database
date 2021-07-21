<template>
  <q-page> </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

// import { SetDetail } from "@/components";
// import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Set",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    // SuspenseWithError,
    // SetDetail,
  },
  setup(props) {
    // TODO: We want to use the name here...
    useMeta({ title: `Set ${props.objId}` });
    provide("objId", props.objId);
  },
});
</script>
