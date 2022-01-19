<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-item :class="colour">
        <q-item-section avatar>
          <q-avatar icon="subject"> </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h5">
            <template v-if="!loading">
              {{ ticket.subject }} #{{ id }}
            </template>
            <template v-else>
              <q-skeleton width="30rem" />
            </template>
          </q-item-label>
          <q-item-label v-if="subheading" caption>
            {{ subheading }}
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <p v-if="!loading" class="text-body1">
          {{ ticket.description || "No description provided." }}
        </p>
        <q-skeleton v-else height="10rem" square />
        <q-badge v-if="ticket.tags" outline color="primary">
          {{ ticket.tags }}
        </q-badge>
      </q-card-section>
      <OpaqueSpinner :showing="loading" />
    </q-card>

    <Attachments v-if="attachment" />
    <Comments />
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, onMounted, readonly, ref, provide } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { Attachments, Comments } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { ticketDetailSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "TicketDetail",
  components: {
    Attachments,
    Comments,
    OpaqueSpinner,
  },
  setup(_, context) {
    const $route = useRoute();
    const { loading, success, data, fetchAPI } = useAPI(context);

    const id = ref($route.params.id);
    const model = "Ticket";

    const attachment = ref(null);
    const colour = ref("");
    const ticket = ref({});
    const subheading = ref("");

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    useMeta({ title: `Ticket #${id.value}` });

    const fetchData = async () => {
      await fetchAPI(requests.tickets.getTicket(id.value));
      if (success.value);
      await ticketDetailSchema
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          subheading.value =
            `${value.creationUser.fullName} opened this issue` +
            ` on ${value.creationTimestamp}`;
          colour.value = value.status
            ? "bg-green-5 text-grey-1"
            : "bg-red-12 text-grey-1";
          ticket.value = value;
          attachment.value = value.file;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());

    return { attachment, colour, loading, subheading, ticket, id };
  },
});
</script>
