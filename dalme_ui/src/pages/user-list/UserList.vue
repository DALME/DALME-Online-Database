<template>
  <Page>
    <SuspenseWithError>
      <template #default>
        <Users />
      </template>
    </SuspenseWithError>
  </Page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Page, Users } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "UserList",
  components: {
    Page,
    SuspenseWithError,
    Users,
  },
  setup() {
    useMeta({ title: "Users" });
  },
});
</script>
