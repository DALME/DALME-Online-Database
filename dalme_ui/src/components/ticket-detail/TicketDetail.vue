<template>
  <div class="q-ma-md full-width full-height">
    <q-card
      class="q-ma-md"
      :class="[isNil(completed) ? null : completed ? 'complete' : 'incomplete']"
    >
      <q-item>
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

      <q-separator />

      <q-card-actions v-if="isAdmin">
        <q-btn @click.stop="onAction" flat>{{ action }}</q-btn>
      </q-card-actions>
      <OpaqueSpinner :showing="loading" />
    </q-card>

    <Attachments v-if="attachment" />
    <Comments />
  </div>
</template>

<script>
import { isNil } from "ramda";
import { useMeta } from "quasar";
import {
  computed,
  defineComponent,
  onMounted,
  readonly,
  ref,
  provide,
} from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { requests } from "@/api";
import { Attachments, Comments } from "@/components";
import { OpaqueSpinner } from "@/components/utils";
import { ticketDetailSchema } from "@/schemas";
import { useAPI, useNotifier } from "@/use";

export default defineComponent({
  name: "TicketDetail",
  components: {
    Attachments,
    Comments,
    OpaqueSpinner,
  },
  setup() {
    const model = "Ticket";

    const $notifier = useNotifier();
    const $route = useRoute();
    const $store = useStore();
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const action = ref("");
    const attachment = ref(null);
    const completed = ref(null);
    const ticket = ref({});
    const subheading = ref("");
    const isAdmin = $store.getters["auth/isAdmin"];

    const id = computed(() => $route.params.id);

    useMeta({ title: `Ticket #${id.value}` });

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    const onAction = async () => {
      const { success, fetchAPI, status } = apiInterface();
      const action = ticket.value.status ? "markClosed" : "markOpen";
      await fetchAPI(requests.tickets.setTicketState(id.value, action));
      if (success.value && status.value === 200) {
        $notifier.tickets.ticketStatusUpdated();
        await fetchData();
      } else {
        $notifier.tickets.ticketStatusUpdatedError();
      }
    };

    const fetchData = async () => {
      await fetchAPI(requests.tickets.getTicket(id.value));
      if (success.value);
      await ticketDetailSchema
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          subheading.value =
            `${value.creationUser.fullName} opened this issue` +
            ` on ${value.creationTimestamp}`;
          completed.value = value.status;
          action.value = completed.value ? "reopen ticket" : "close ticket";
          ticket.value = value;
          attachment.value = value.file;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());

    return {
      action,
      attachment,
      completed,
      id,
      isAdmin,
      isNil,
      loading,
      onAction,
      subheading,
      ticket,
    };
  },
});
</script>

<style lang="scss" scoped>
.complete {
  border-top: 10px solid green;
}
.incomplete {
  border-top: 10px solid red;
}
</style>
