<template>
  <Page>
    <router-view />
  </Page>
</template>

<script>
import { defineComponent } from "vue";
import { Page } from "@/components";

export default defineComponent({
  name: "User",
  components: { Page },
});
</script>
