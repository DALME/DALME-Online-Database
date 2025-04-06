<template>
  <q-card v-if="!loading" flat>
    <q-card-section :class="`comment-thread ${dark ? 'dark' : ''} ${worklog ? 'worklog' : ''}`">
      <template v-if="comments.length">
        <template v-for="(entry, idx) in comments" :key="idx">
          <template v-if="'event' in entry">
            <q-item class="event-box" :class="entry.user.id == op ? 'op-post' : ''">
              <q-item-section avatar>
                <q-icon :class="getEventClass(entry.event)" :name="getEventIcon(entry.event)" />
              </q-item-section>
              <div class="event-content">
                <UserPill
                  v-if="!entry.event.startsWith('Automatic')"
                  :user="entry.user"
                  text-size="13px"
                />
                <q-icon
                  color="deep-purple-6"
                  class="avatar-icon"
                  v-else
                  name="smart_toy"
                  size="12px"
                />
                <span v-text="getEventText(entry.event, entry.timestamp)" />
              </div>
            </q-item>
          </template>
          <template v-else>
            <q-item class="comment-box" :class="entry.creationUser.id == op ? 'op-post' : ''">
              <q-item-section v-if="entry.creationUser.id == op" avatar>
                <q-avatar size="40px">
                  <q-img
                    v-if="!nully(entry.creationUser.avatar)"
                    :src="entry.creationUser.avatar"
                    fit="cover"
                    ratio="1"
                  />
                  <q-icon v-else size="36px" name="mdi-account-circle" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-card flat bordered :class="containerClasses(entry.creationUser.id)">
                  <q-card-section class="comment-head">
                    <DetailPopover :dark="dark" :userData="entry.creationUser" :showAvatar="true" />
                    commented {{ formatDate(entry.creationTimestamp) }}
                  </q-card-section>
                  <q-card-section class="q-pa-none">
                    <MarkdownEditor :text="entry.body" :dark="dark" in-card />
                  </q-card-section>
                </q-card>
              </q-item-section>
              <q-item-section v-if="entry.creationUser.id != op" side>
                <q-avatar size="40px">
                  <q-img
                    v-if="!nully(entry.creationUser.avatar)"
                    :src="entry.creationUser.avatar"
                    fit="cover"
                    ratio="1"
                  />
                  <q-icon v-else size="36px" name="mdi-account-circle" />
                </q-avatar>
              </q-item-section>
            </q-item>
          </template>
        </template>
      </template>

      <slot name="comment-stream-end" />
      <q-separator v-if="comments.length > 0" class="comment-thread-divider" />
    </q-card-section>
    <q-card-section
      :class="`comment-thread ${dark ? 'dark' : ''} ${auth.user.userId == op ? 'op' : 'not-op'}`"
    >
      <q-item class="comment-box" :class="auth.user.userId == op ? 'op-post' : ''">
        <q-item-section v-if="auth.user.userId == op" avatar>
          <q-avatar size="40px">
            <q-img v-if="!nully(auth.user.avatar)" :src="auth.user.avatar" fit="cover" ratio="1" />
            <q-icon v-else size="36px" name="mdi-account-circle" />
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <MarkdownEditor
            ref="commentEditor"
            editable
            placeholder="Leave a comment..."
            :help="helpLine"
            submit-label="Comment"
            @on-save-text="onSubmit"
            :dark="dark"
            :right="auth.user.userId != op"
          />
        </q-item-section>
        <q-item-section v-if="auth.user.userId != op" side>
          <q-avatar size="40px">
            <q-img v-if="!nully(auth.user.avatar)" :src="auth.user.avatar" fit="cover" ratio="1" />
            <q-icon v-else size="36px" name="mdi-account-circle" />
          </q-avatar>
        </q-item-section>
      </q-item>
    </q-card-section>
  </q-card>
  <AdaptiveSpinner v-else class="q-ma-auto" />
</template>

<script>
import { defineComponent, inject, onMounted, ref, watch } from "vue";
import { API as apiInterface, requests } from "@/api";
import MarkdownEditor from "@/components/markdown-editor/MarkdownEditor.vue";
import { AdaptiveSpinner, DetailPopover } from "@/components/widgets";
import { formatDate, nully } from "@/utils";
import { commentPayloadSchema, commentsSchema, commentSchema } from "@/schemas";
import { useAuthStore } from "@/stores/auth";
import notifier from "@/notifier";
import { useConstants } from "@/use";
import { UserPill } from "@/components";

export default defineComponent({
  name: "CommentBox",
  props: {
    author: {
      type: Number,
      required: false,
    },
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
    worklog: Array,
  },
  components: {
    AdaptiveSpinner,
    DetailPopover,
    MarkdownEditor,
    UserPill,
  },
  emits: ["onCountChanged"],
  setup(props, context) {
    const auth = useAuthStore();
    const { loading, success, status, data, fetchAPI } = apiInterface();
    const { workflowIconbyLabel } = useConstants();
    const comments = ref([]);
    const commentEditor = ref(null);
    const submitting = ref(false);
    const helpLine = "Add a new comment to the thread. Markdown styling is supported.";
    const model = inject("model");
    const id = inject("id");
    const op = ref(0);

    const containerClasses = (commentAuthor) => {
      let clss = commentAuthor == op.value ? "box-arrow" : "box-arrow right";
      return props.dark ? (clss += " dark") : clss;
    };

    const onSubmit = async (text) => {
      submitting.value = true;
      const payload = { model, body: text, object: id.value };
      await commentPayloadSchema.validate(payload).then(async () => {
        const request = requests.comments.addComment(payload);
        await fetchAPI(request);
        if (status.value == 201) {
          await commentSchema.validate(data.value).then((value) => {
            comments.value.push(value);
            context.emit("onCountChanged", comments.value.length);
            notifier.comments.commentAdded();
          });
        } else {
          notifier.comments.commentFailed();
        }
      });
      loading.value = false;
      submitting.value = false;
    };

    const sortFunction = (valA, valB) => {
      const a = valA.creationTimestamp?.iso8601 || valA.timestamp?.iso8601;
      const b = valB.creationTimestamp?.iso8601 || valB.timestamp?.iso8601;
      return a < b ? -1 : a > b ? 1 : 0;
    };

    const getEventClass = (event) => {
      const classes = {
        public: "publication",
        Automatic: "automatic",
        help: "help-flag",
        status: "assessment",
      };
      const isTrue = event.endsWith("True");
      return event.split(" ")[0] in classes
        ? `event-icon ${classes[event.split(" ")[0]]} ${isTrue ? "true" : ""}`
        : "event-icon";
    };

    const getEventIcon = (event) => {
      const icons = {
        Source: "add_circle_outline",
        public: "public",
        Automatic: "lightbulb_circle",
        help: "flag_circle",
        status: "error_outline",
      };
      return event.includes(":")
        ? workflowIconbyLabel[event.substring(0, event.indexOf(":"))]
        : icons[event.split(" ")[0]];
    };

    const getEventText = (event, timestamp = null) => {
      let text = "";
      if (event.startsWith("Automatic")) {
        text = event;
      } else if (event.startsWith("Source")) {
        text = "created this record";
      } else if (event.startsWith("public")) {
        text = event.endsWith("True") ? "published this record" : "unpublished this record";
      } else if (event.startsWith("help")) {
        text = event.endsWith("True")
          ? "set the help flag for this record"
          : "unset the help flag for this record";
      } else if (event.startsWith("status")) {
        // eslint-disable-next-line quotes
        text = event.endsWith('"processing"')
          ? "placed this record back into the processing workflow"
          : "placed this record under assessment";
      } else {
        const action = event.substring(0, event.indexOf(":"));
        const verb = event.endsWith("commenced") ? "started" : "completed";
        text = `${verb} ${action} of this record`;
      }
      return timestamp ? `${text} on ${timestamp.date} @ ${timestamp.time}` : text;
    };

    const fetchData = async () => {
      await fetchAPI(requests.comments.getComments(model, id.value));
      if (success.value) {
        await commentsSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          if (nully(props.worklog)) {
            comments.value = value.data;
            if (props.author || value.count > 0) {
              op.value = props.author || value.data[0].creationUser.id;
            }
          } else {
            comments.value = value.data.concat(props.worklog).sort(sortFunction);
            op.value = props.worklog[0].user.id;
          }
          loading.value = false;
        });
      }
    };

    onMounted(async () => {
      await fetchData();
    });

    watch(
      () => id.value,
      () => fetchData(),
    );

    return {
      op,
      auth,
      comments,
      loading,
      formatDate,
      commentEditor,
      helpLine,
      onSubmit,
      nully,
      containerClasses,
      getEventIcon,
      getEventText,
      getEventClass,
    };
  },
});
</script>

<style lang="scss">
.comment-thread {
  --bg-colour: var(--light-bg-base-colour);
  --bg-raised: var(--light-bg-raised-colour);
  --border-colour: var(--ligth-border-base-colour);
  --blue-box: var(--light-blue-box-colour);
  --blue-text: var(--light-blue-box-text);
  --green-box: var(--light-green-box-colour);
  --green-text: var(--light-green-box-text);
  --secondary-colour: var(--light-secondary-text-colour);
  --green-button: var(--light-green-button-bg);
  --green-button-text: var(--light-green-button-text);
}
.comment-thread.dark {
  --bg-colour: var(--dark-bg-base-colour);
  --bg-raised: var(--dark-bg-raised-colour);
  --border-colour: var(--dark-border-base-colour);
  --blue-box: var(--dark-blue-box-colour);
  --blue-text: var(--dark-blue-box-text);
  --green-box: var(--dark-green-box-colour);
  --green-text: var(--dark-green-box-text);
  --secondary-colour: var(--dark-secondary-text-colour);
  --green-button: var(--dark-green-button-bg);
  --green-button-text: var(--dark-green-button-text);
}
.comment-thread {
  padding: 0;
  background:
    linear-gradient(to right, #00000000 0 48%, var(--blue-box) 49% 52%, #00000000 53% 100%)
      no-repeat content-box left/40px 100%,
    linear-gradient(to left, #00000000 0 48%, var(--green-box) 49% 52%, #00000000 53% 100%)
      no-repeat content-box right/40px 100%;
}
.comment-thread.not-op {
  padding: 0;
  background: linear-gradient(
      to left,
      #00000000 0 48%,
      var(--green-box) 49% 52%,
      #00000000 53% 100%
    )
    no-repeat right/40px 100%;
}
.comment-thread.op {
  padding: 0;
  background: linear-gradient(
      to right,
      #00000000 0 48%,
      var(--blue-box) 49% 52%,
      #00000000 53% 100%
    )
    no-repeat left/40px 100%;
}
.comment-thread.worklog {
  padding-top: 20px;
}
.q-pt-20 {
  padding-top: 20px !important;
}
.comment-box {
  padding: 0 0 15px 0;
}
.event-box {
  padding: 0 0 0 6px;
}
.event-box + .comment-box {
  padding-top: 15px;
}
.event-box:first-of-type {
  margin-top: -20px;
}
.event-box:last-of-type {
  padding-bottom: 15px;
}
.comment-box:not(.op-post) {
  margin-left: auto;
}
.comment-box .q-card:not(.md-editor-container) {
  border-color: var(--green-box);
}
.comment-box.op-post .q-card:not(.md-editor-container) {
  border-color: var(--blue-box);
}
.comment-box .q-card__section:not(.comment-head) {
  padding-bottom: 0;
  min-height: 58px;
}
.comment-box .q-item__section--avatar {
  padding-right: 18px;
}
.comment-box .q-item__section--side:not(.q-item__section--avatar) {
  padding-left: 18px;
}
.event-box .q-avatar .q-avatar__content,
.event-box .avatar-icon,
.comment-box .q-avatar:not(.closing-dot) .q-avatar__content {
  background-color: var(--bg-colour);
  border: 2px solid var(--green-box);
}
.event-box.op-post .q-avatar .q-avatar__content,
.event-box.op-post .avatar-icon,
.comment-box.op-post .q-avatar:not(.closing-dot) .q-avatar__content {
  border: 2px solid var(--blue-box);
}
.comment-box .q-avatar:not(.closing-dot) .q-icon {
  color: var(--secondary-colour);
}
.comment-box.op-post .q-avatar__content .q-icon {
  color: var(--blue-box) !important;
}
.comment-box .q-avatar__content .q-icon {
  color: var(--green-box) !important;
}
.comment-thread-divider {
  background: var(--border-colour) !important;
  height: 2px;
  position: relative;
  border-bottom: 24px solid var(--bg-colour);
}
.comment-box .comment-head {
  height: 32px;
  display: flex;
  justify-content: flex-start;
  white-space: pre;
  font-size: 13px;
  align-items: center;
  border-bottom: 1px solid;
  border-color: inherit;
  padding: 0 16px;
  background: var(--green-box);
  color: var(--green-text);
  border-radius: unset !important;
}
.comment-box.op-post .comment-head {
  background: var(--blue-box) !important;
  color: var(--blue-text) !important;
}
.comment-box .q-avatar.closing-dot {
  width: 32px;
  height: 32px;
  position: relative;
  background: #558b2f;
  right: 5px;
}
.comment-box.op-post .q-avatar.closing-dot {
  left: 5px;
}
.comment-thread-divider + .comment-box {
  padding-top: 28px;
  padding-bottom: 28px;
  margin-bottom: 24px;
}
.event-icon {
  font-size: 18px !important;
  color: var(--blue-text);
  background-color: #d1e4f9;
  border: 2px solid var(--bg-colour);
  border-radius: 18px;
  padding: 3px;
}
.event-icon.publication {
  color: #700c0c;
  background-color: #e1b7b7;
}
.event-icon.publication.true {
  color: #0c700c;
  background-color: #b7e1be;
}
.event-icon.automatic {
  color: #6b6b6b;
  background-color: #dfdfdf;
}
.event-icon.help-flag {
  color: #9c4d19;
  background-color: #e1ceb7;
}
.event-icon.assessment {
  color: #8a8111;
  background-color: #e2e1ab;
}
.event-content {
  font-size: 13px;
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  padding-right: 40px;
  line-height: 1.3;
}
.avatar-icon {
  border-radius: 14px;
  padding: 1px;
  margin-right: 5px;
}
</style>
