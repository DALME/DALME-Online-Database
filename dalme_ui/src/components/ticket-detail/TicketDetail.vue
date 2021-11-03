<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-item :class="colour">
        <q-item-section avatar>
          <q-avatar icon="subject"> </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h5">
            {{ ticket.subject }}
            <span>#{{ id }}</span>
          </q-item-label>
          <q-item-label caption>{{ subheading }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <p class="text-body1">{{ ticket.description }}</p>
        <q-badge v-if="ticket.tags" outline color="primary">
          {{ ticket.tags }}
        </q-badge>
      </q-card-section>
    </q-card>

    <Attachments v-if="attachment" />
    <Comments />
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent, readonly, ref, provide } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { Attachments, Comments } from "@/components";
import { ticketDetailSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "TicketDetail",
  components: {
    Attachments,
    Comments,
  },
  async setup(_, context) {
    const $route = useRoute();
    const { success, data, fetchAPI } = useAPI(context);

    let subheading = "";
    const model = "Ticket";
    const attachment = ref("");
    const colour = ref("");
    const ticket = ref(null);
    const id = ref($route.params.id);

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
          subheading =
            `${value.creationUser.fullName} opened this issue` +
            ` on ${value.creationTimestamp}`;
          colour.value = value.status
            ? "bg-green-5 text-grey-1"
            : "bg-red-12 text-grey-1";
          ticket.value = value;
          attachment.value = value.file;
        });
    };

    await fetchData();

    return { attachment, colour, subheading, ticket, id };
  },
});
</script>
