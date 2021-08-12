<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <Users />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";

import { Users } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "UserList",
  components: {
    SuspenseWithError,
    Users,
  },
  setup() {
    useMeta({ title: "Users" });
  },
});
</script>
