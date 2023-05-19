<template>
  <div
    v-if="!loading && !isEmpty(ticket)"
    class="full-width full-height q-px-content-visual"
  >
    <div class="info-area row">
      <div class="col-grow">
        <div class="row items-center text-h5">
          {{ ticket.subject }}
          <span class="q-ml-sm text-grey-7">#{{ id }}</span>
        </div>
        <div class="row detail-row-subheading text-grey-8">
          <q-chip
            :icon="ticket.status ? 'o_check_circle' : 'o_error_outline'"
            :label="ticket.status ? 'Closed' : 'Open'"
            :color="ticket.status ? 'deep-purple-6' : 'green-7'"
            text-color="white"
            size="sm"
            class="q-ml-none q-mr-xs"
          />
          <DetailPopover :userData="ticket.creationUser" :showAvatar="false" />
          created this ticket {{ formatDate(ticket.creationTimestamp) }}
        </div>
      </div>
      <div v-if="isAdmin" class="col-auto">
        <q-btn
          dense
          outline
          no-caps
          :color="buttonColours.colour"
          :class="`action-button bg-${buttonColours.colour}`"
          :text-color="buttonColours.text"
          :label="capitalize(action)"
          @click.stop="onAction"
        />
      </div>
    </div>
    <q-separator class="q-mb-lg" />
    <div class="row">
      <div class="col-9 q-pr-md">
        <q-card flat class="q-mb-md">
          <q-card-section
            :class="
              ticket.commentCount > 0
                ? 'q-pt-none q-pr-none'
                : 'q-pt-none q-pr-none comments-container'
            "
          >
            <div class="comment_thread q-mt-none q-pb-lg">
              <q-item class="q-pb-sm q-pt-none q-px-none">
                <q-item-section top avatar>
                  <q-avatar v-if="ticket.creationUser.avatar" size="40px">
                    <img :src="ticket.creationUser.avatar" />
                  </q-avatar>
                  <q-avatar
                    v-else
                    size="40px"
                    icon="account_circle"
                    color="grey-4"
                    text-color="grey-6"
                  />
                </q-item-section>
                <q-item-section>
                  <q-card flat bordered class="box-left-arrow">
                    <q-card-section class="bg-grey-2 comment-head">
                      <DetailPopover
                        :userData="ticket.creationUser"
                        :showAvatar="false"
                      />
                      commented {{ formatDate(ticket.creationTimestamp) }}
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="text-body2">
                      <MarkdownEditor
                        v-if="ticket.description"
                        :text="ticket.description"
                      />
                      <span v-else>No description provided.</span>
                    </q-card-section>
                  </q-card>
                </q-item-section>
              </q-item>
            </div>
            <Comments>
              <template v-if="ticket.status" v-slot:comment-stream-end>
                <div class="comment_thread row items-center q-mt-none q-pb-lg">
                  <div class="closing-dot bg-deep-purple-6">
                    <q-icon name="o_check_circle" color="white" size="20px" />
                  </div>
                  <div class="closing-dot-label">
                    <DetailPopover :userData="ticket.closingUser" />
                    closed this ticket {{ formatDate(ticket.closingDate) }}
                  </div>
                </div>
              </template>
            </Comments>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-3 q-pl-md">
        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
          Assignees
        </div>
        <div class="q-mb-sm text-13">
          <span>No one assigned</span>
        </div>
        <q-separator class="q-my-md" />

        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">Tags</div>
        <div class="q-mb-sm text-13">
          <template v-if="!isEmpty(cleanTags(ticket.tags))">
            <Tag
              v-for="(tag, idx) in cleanTags(ticket.tags)"
              :key="idx"
              :name="tag.tag"
              :type="tag.tag"
              size="xs"
              module="ticket"
              class="q-ml-sm"
            />
          </template>
          <span v-else>None yet</span>
        </div>
        <q-separator class="q-my-md" />

        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
          Attachments
        </div>
        <div class="q-mb-sm text-13">
          <Attachments v-if="attachment" />
          <span v-else>None yet</span>
        </div>
        <q-separator class="q-my-md" />

        <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
          Links
        </div>
        <div class="q-mb-sm text-13">
          <span>None yet</span>
        </div>
      </div>
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { filter as rFilter, isEmpty, isNil } from "ramda";
import { useMeta, format } from "quasar";
import {
  computed,
  defineComponent,
  onMounted,
  readonly,
  ref,
  provide,
} from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import { Attachments, Comments, MarkdownEditor } from "@/components";
import {
  DetailPopover,
  formatDate,
  OpaqueSpinner,
  Tag,
} from "@/components/utils";
import { ticketDetailSchema } from "@/schemas";
import { useAPI, useEventHandling, useStores } from "@/use";

export default defineComponent({
  name: "TicketDetail",
  components: {
    Attachments,
    Comments,
    DetailPopover,
    MarkdownEditor,
    OpaqueSpinner,
    Tag,
  },
  setup() {
    const { notifier } = useEventHandling();
    const $route = useRoute();
    const { isAdmin, nav } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { capitalize } = format;
    const model = "Ticket";
    const action = ref("");
    const attachment = ref(null);
    const ticket = ref({});
    const id = computed(() => $route.params.id);
    const buttonColours = computed(() =>
      action.value === "reopen ticket"
        ? { colour: "green-1", text: "green-7" }
        : { colour: "deep-purple-1", text: "deep-purple-6" },
    );

    useMeta({ title: `Ticket #${id.value}` });
    nav.breadcrumbTail.push(`#${id.value}`);

    provide("attachment", attachment);
    provide("model", model);
    provide("id", readonly(id));

    const onAction = async () => {
      const { success, fetchAPI, status } = apiInterface();
      const action = ticket.value.status ? "markClosed" : "markOpen";
      await fetchAPI(requests.tickets.setTicketState(id.value, action));
      if (success.value && status.value === 200) {
        notifier.tickets.ticketStatusUpdated();
        await fetchData();
      } else {
        notifier.tickets.ticketStatusUpdatedError();
      }
    };

    const cleanTags = (tags) => {
      return rFilter((tag) => tag.tag, tags);
    };

    const fetchData = async () => {
      await fetchAPI(requests.tickets.getTicket(id.value));
      if (success.value)
        await ticketDetailSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            action.value = value.status ? "reopen ticket" : "close ticket";
            ticket.value = value;
            attachment.value = value.file;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    onBeforeRouteLeave(() => {
      nav.resetBreadcrumbTail();
    });

    return {
      action,
      attachment,
      buttonColours,
      capitalize,
      cleanTags,
      formatDate,
      id,
      isAdmin,
      isEmpty,
      isNil,
      loading,
      onAction,
      ticket,
    };
  },
});
</script>

<style lang="scss">
.closing-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  justify-content: center;
  flex-shrink: 0;
  align-items: center;
  display: inline-flex;
  position: relative;
  left: 55px;
}
.closing-dot-label {
  padding-left: 65px;
  padding-bottom: 2px;
}
.action-button {
  padding: 0px 10px 0px 10px;
  font-weight: 600;
  font-size: 14px;
}
</style>
