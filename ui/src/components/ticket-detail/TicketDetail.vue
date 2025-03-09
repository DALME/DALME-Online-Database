<template>
  <div v-if="!loading && !isEmpty(ticket)" class="full-width full-height q-px-content-visual">
    <div class="info-area row">
      <div class="col-grow">
        <div class="row items-center text-h5">
          {{ ticket.subject }}
          <span class="q-ml-sm text-grey-7">#{{ number }}</span>
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
      <div class="col-9 q-pr-lg">
        <q-card flat class="q-mb-md">
          <q-card-section
            :class="
              ticket.commentCount > 0
                ? 'q-pt-none q-pr-none'
                : 'q-pt-none q-pr-none comments-container'
            "
          >
            <div class="comment-thread q-mt-none q-pb-lg">
              <q-item class="q-pb-sm q-pt-none q-px-none comment-box op-post">
                <q-item-section top avatar>
                  <q-avatar size="40px">
                    <q-img
                      v-if="!nully(ticket.creationUser.avatar)"
                      :src="ticket.creationUser.avatar"
                      fit="cover"
                      ratio="1"
                    />
                    <q-icon v-else size="36px" name="mdi-account-circle" />
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-card flat bordered class="box-arrow top">
                    <q-card-section class="bg-grey-2 comment-head">
                      <DetailPopover :userData="ticket.creationUser" :showAvatar="false" />
                      commented {{ formatDate(ticket.creationTimestamp) }}
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="text-body2 q-pa-none">
                      <MarkdownEditor
                        v-if="ticket.description"
                        :text="ticket.description"
                        in-card
                      />
                      <span v-else>No description provided.</span>
                    </q-card-section>
                  </q-card>
                </q-item-section>
              </q-item>
            </div>
            <CommentBox>
              <template v-if="ticket.status" v-slot:comment-stream-end>
                <div class="comment-thread row items-center q-mt-none q-pb-lg">
                  <div class="closing-dot bg-deep-purple-6">
                    <q-icon name="o_check_circle" color="white" size="20px" />
                  </div>
                  <div class="closing-dot-label">
                    <DetailPopover :userData="ticket.closingUser" />
                    closed this ticket {{ formatDate(ticket.closingDate) }}
                  </div>
                </div>
              </template>
            </CommentBox>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-3 q-pl-md">
        <DetailSidebar>
          <template v-slot:extraElements>
            <DetailElement label="Assignee">
              <template v-slot:content>
                <template v-if="ticket.assignedTo">
                  <router-link
                    :to="{
                      name: 'User',
                      params: { username: ticket.assignedTo.username },
                    }"
                  >
                    {{ ticket.assignedTo.fullName }}
                  </router-link>
                </template>
                <div class="text-13" v-else>No one assigned</div>
              </template>
            </DetailElement>
            <DetailElement label="Tags">
              <template v-slot:content>
                <template v-if="!isEmpty(cleanTags(ticket.tags))">
                  <TagPill
                    v-for="(tag, idx) in cleanTags(ticket.tags)"
                    :key="idx"
                    :name="tag.tag"
                    :type="tag.tag"
                    size="xs"
                    module="ticket"
                    class="q-ml-sm"
                  />
                </template>
                <div class="text-13" v-else>None yet</div>
              </template>
            </DetailElement>
            <DetailElement label="Attachments">
              <template v-slot:content>
                <template v-if="!isEmpty(ticket.files)">
                  <AttachmentWidget v-for="file in ticket.files" :key="file.id" :file="file" />
                </template>
                <div class="text-13" v-else>None yet</div>
              </template>
            </DetailElement>
            <DetailElement label="Link">
              <template v-slot:content>
                <template v-if="ticket.url">
                  <ExternalLink :url="ticket.url" />
                </template>
                <div class="text-13" v-else>None yet</div>
              </template>
            </DetailElement>
          </template>
        </DetailSidebar>
      </div>
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { filter as rFilter, isEmpty, isNil } from "ramda";
import { useMeta, format } from "quasar";
import { computed, defineComponent, onMounted, readonly, ref, provide } from "vue";
import { onBeforeRouteLeave, useRoute } from "vue-router";
import { requests } from "@/api";
import {
  AttachmentWidget,
  CommentBox,
  DetailSidebar,
  DetailElement,
  DetailPopover,
  ExternalLink,
  MarkdownEditor,
  OpaqueSpinner,
  TagPill,
} from "@/components";
import { formatDate, nully } from "@/utils";
import { ticketSchema } from "@/schemas";
import { useAPI, useEventHandling, useStores } from "@/use";

export default defineComponent({
  name: "TicketDetail",
  components: {
    AttachmentWidget,
    CommentBox,
    DetailSidebar,
    DetailElement,
    DetailPopover,
    ExternalLink,
    MarkdownEditor,
    OpaqueSpinner,
    TagPill,
  },
  setup() {
    const { notifier } = useEventHandling();
    const $route = useRoute();
    const { auth, ui } = useStores();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const { capitalize } = format;
    const model = "Ticket";
    const action = ref("");
    const attachment = ref(null);
    const ticket = ref({});
    const id = ref(null);
    const number = computed(() => $route.params.id);
    const buttonColours = computed(() =>
      action.value === "reopen ticket"
        ? { colour: "green-1", text: "green-7" }
        : { colour: "deep-purple-1", text: "deep-purple-6" },
    );

    useMeta({ title: `Ticket #${number.value}` });
    ui.breadcrumbTail.push(`#${number.value}`);

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
      await fetchAPI(requests.tickets.getTicket(number.value));
      if (success.value)
        await ticketSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          action.value = value.status ? "reopen ticket" : "close ticket";
          ticket.value = value;
          attachment.value = value.file;
          id.value = value.id;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());

    onBeforeRouteLeave(() => {
      ui.resetBreadcrumbTail();
    });

    return {
      action,
      attachment,
      buttonColours,
      capitalize,
      cleanTags,
      formatDate,
      number,
      isAdmin: auth.user.isAdmin,
      isEmpty,
      isNil,
      loading,
      onAction,
      ticket,
      nully,
    };
  },
});
</script>

<style lang="scss">
.action-button {
  padding: 0px 10px 0px 10px;
  font-weight: 600;
  font-size: 14px;
}
</style>
