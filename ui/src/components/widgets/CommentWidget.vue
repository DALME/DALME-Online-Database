<template>
  <q-card v-if="!loading" flat>
    <q-card-section :class="threadClasses">
      <template v-if="comments.length">
        <div v-for="(comment, idx) in comments" :key="idx">
          <q-item class="comment-box" :class="comment.creationUser.id == op ? 'op-post' : ''">
            <q-item-section v-if="comment.creationUser.id == op" avatar>
              <q-avatar size="40px">
                <img
                  v-if="!nully(comment.creationUser.avatar)"
                  :src="comment.creationUser.avatar"
                />
                <q-icon v-else size="38px" name="mdi-account-circle" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-card flat bordered :class="containerClasses(comment.creationUser.id)">
                <q-card-section class="comment-head">
                  <DetailPopover :dark="dark" :userData="comment.creationUser" :showAvatar="true" />
                  commented {{ formatDate(comment.creationTimestamp) }}
                </q-card-section>
                <q-card-section>
                  <MarkdownEditor :text="comment.body" :dark="dark" />
                </q-card-section>
              </q-card>
            </q-item-section>
            <q-item-section v-if="comment.creationUser.id != op" side>
              <q-avatar size="40px">
                <img
                  v-if="!nully(comment.creationUser.avatar)"
                  :src="comment.creationUser.avatar"
                />
                <q-icon v-else size="38px" name="mdi-account-circle" />
              </q-avatar>
            </q-item-section>
          </q-item>
        </div>
      </template>

      <slot name="comment-stream-end" />

      <q-separator v-if="comments.length > 0" class="comment-thread-divider" />

      <q-item class="comment-box" :class="auth.user.userId == op ? 'op-post' : ''">
        <q-item-section v-if="auth.user.userId == op" avatar>
          <q-avatar size="40px">
            <img v-if="!nully(auth.user.avatar)" :src="auth.avatar" />
            <q-icon v-else size="38px" name="mdi-account-circle" />
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
            <img v-if="!nully(auth.user.avatar)" :src="auth.avatar" />
            <q-icon v-else size="38px" name="mdi-account-circle" />
          </q-avatar>
        </q-item-section>
      </q-item>
    </q-card-section>
  </q-card>
  <AdaptiveSpinner v-else />
</template>

<script>
import { computed, defineComponent, inject, onMounted, ref, watch } from "vue";
import { API as apiInterface, requests } from "@/api";
import MarkdownEditor from "@/components/markdown-editor/MarkdownEditor.vue";
import { AdaptiveSpinner, DetailPopover } from "@/components/widgets";
import { formatDate, nully } from "@/utils";
import { commentPayloadSchema, commentsSchema, commentSchema } from "@/schemas";
import { useAuthStore } from "@/stores/auth";
import notifier from "@/notifier";

export default defineComponent({
  name: "CommentWidget",
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
  },
  components: {
    DetailPopover,
    MarkdownEditor,
    AdaptiveSpinner,
  },
  emits: ["onCountChanged"],
  setup(props, context) {
    const auth = useAuthStore();
    const { loading, success, status, data, fetchAPI } = apiInterface();
    const comments = ref([]);
    const commentEditor = ref(null);
    const submitting = ref(false);
    const helpLine = "Add a new comment to the thread. Markdown styling is supported.";
    const model = inject("model");
    const id = inject("id");
    const op = ref(0);

    const threadClasses = computed(() => {
      let clss = comments.value.length > 0 ? "comment_thread q-pt-20" : "comment_thread";
      return props.dark ? (clss += " dark") : clss;
    });

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

    const fetchData = async () => {
      await fetchAPI(requests.comments.getComments(model, id.value));
      if (success.value)
        await commentsSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          comments.value = value.data;
          if (props.author || value.count > 0) {
            op.value = props.author || value.data[0].creationUser.id;
          }
          loading.value = false;
        });
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
      threadClasses,
    };
  },
});
</script>

<style lang="scss">
.comment_thread {
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
.comment_thread.dark {
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
.comment_thread {
  padding: 0;
  background:
    linear-gradient(to right, #00000000 0 48%, var(--blue-box) 49% 52%, #00000000 53% 100%)
      no-repeat left/40px 100%,
    linear-gradient(to left, #00000000 0 48%, var(--green-box) 49% 52%, #00000000 53% 100%)
      no-repeat right/40px 100%;
}
.q-pt-20 {
  padding-top: 20px !important;
}
.comment-box {
  padding: 0 0 28px 0;
  max-width: calc(100% - 120px);
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
.comment-box .q-avatar:not(.closing-dot) .q-avatar__content {
  background-color: var(--bg-colour);
  border: 2px solid var(--green-box);
}
.comment-box.op-post .q-avatar:not(.closing-dot) .q-avatar__content {
  border: 2px solid var(--blue-box);
}
.comment-box .q-avatar:not(.closing-dot) .q-icon {
  color: var(--secondary-colour);
}
.comment-thread-divider {
  background: var(--border-colour) !important;
  height: 1px;
  position: relative;
  border-bottom: 24px solid var(--bg-colour);
  border-top: 24px solid var(--bg-colour);
  right: -43px;
  left: -43px;
  width: 110%;
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
</style>
