<template>
  <q-page> </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

// import { UserDetail } from "@/components";
// import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "User",
  props: {
    username: {
      type: String,
      required: true,
    },
  },
  components: {
    // SuspenseWithError,
    // UserDetail,
  },
  setup(props) {
    useMeta({ title: `User: ${props.username}` });
    provide("objId", props.username);
  },
});
</script>
