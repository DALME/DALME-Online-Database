<template>
  <q-page>
    <SuspenseWithError>
      <template #default>
        <TicketDetail />
      </template>
    </SuspenseWithError>
  </q-page>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, provide } from "vue";

import { TicketDetail } from "@/components";
import { SuspenseWithError } from "@/components/utils";

export default defineComponent({
  name: "Ticket",
  props: {
    objId: {
      type: String,
      required: true,
    },
  },
  components: {
    SuspenseWithError,
    TicketDetail,
  },
  setup(props) {
    useMeta({ title: `Ticket #${props.objId}` });
    provide("objId", props.objId);
    provide("model", "Ticket");
  },
});
</script>
