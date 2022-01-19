<template>
  <Page>
    <Users />
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Users } from "@/components";

export default defineComponent({
  name: "UserList",
  components: {
    Page,
    Users,
  },
  setup() {
    useMeta({ title: "Users" });
  },
});
</script>
