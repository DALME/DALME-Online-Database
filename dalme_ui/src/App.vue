<template>
  <router-view />
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  setup() {
    useMeta({ titleTemplate: (title) => `${title} | DALME` });
  },
});
</script>
