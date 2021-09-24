<template>
  <q-page>
    <div class="full-width full-height">
      <SetDetail />
      <Comments />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, provide, ref } from "vue";
import { useRoute } from "vue-router";

import { Comments, SetDetail } from "@/components";

export default defineComponent({
  name: "Set",
  components: {
    Comments,
    SetDetail,
  },
  setup() {
    const $route = useRoute();

    const objId = ref($route.params.objId);

    provide("model", "Set");
    provide("objId", objId);
  },
});
</script>
