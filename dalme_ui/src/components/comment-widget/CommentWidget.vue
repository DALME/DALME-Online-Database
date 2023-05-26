<template>
  <q-card v-if="!loading" flat>
    <q-card-section v-if="comments.length" class="comments-container">
      <div
        v-for="(comment, idx) in comments"
        :key="idx"
        class="comment_thread q-mt-none q-pb-lg"
      >
        <q-item class="q-pb-sm q-pt-none q-px-none">
          <q-item-section top avatar>
            <q-avatar v-if="comment.creationUser.avatar" size="40px">
              <img :src="comment.creationUser.avatar" />
            </q-avatar>
            <q-avatar
              v-else
              size="40px"
              icon="account_circle"
              color="light-blue-3"
              text-color="blue-9"
            />
          </q-item-section>
          <q-item-section>
            <q-card flat bordered class="box-left-arrow">
              <q-card-section
                class="comment-head bg-grey-2 q-py-none flex-center"
              >
                <DetailPopover
                  :userData="comment.creationUser"
                  :showAvatar="false"
                />
                commented {{ formatDate(comment.creationTimestamp) }}
              </q-card-section>
              <q-separator />
              <q-card-section class="text-body2">
                <MarkdownEditor :text="comment.body" />
              </q-card-section>
            </q-card>
          </q-item-section>
        </q-item>
      </div>
      <slot name="comment-stream-end" />
    </q-card-section>
    <q-card-section class="q-pt-sm q-px-none">
      <q-item class="q-py-sm q-px-none">
        <q-item-section top avatar>
          <q-avatar v-if="auth.avatar" size="40px">
            <img :src="auth.avatar" />
          </q-avatar>
          <q-avatar
            v-else
            size="40px"
            icon="account_circle"
            color="light-blue-3"
            text-color="blue-9"
          />
        </q-item-section>
        <q-item-section>
          <MarkdownEditor
            ref="commentEditor"
            editable
            placeholder="Leave a comment..."
            :help="helpLine"
            submitLabel="Comment"
            @on-save-text="onSubmit"
          />
        </q-item-section>
      </q-item>
    </q-card-section>
  </q-card>
  <AdaptiveSpinner v-else />
</template>

<script>
import { defineComponent, inject, onMounted, ref } from "vue";
import { requests } from "@/api";
import { MarkdownEditor } from "@/components";
import { DetailPopover } from "@/components/utils";
import { formatDate, AdaptiveSpinner } from "@/components/utils";
import { commentPayloadSchema, commentsSchema, commentSchema } from "@/schemas";
import { useAPI, useEventHandling, useStores } from "@/use";

export default defineComponent({
  name: "CommentWidget",
  components: {
    DetailPopover,
    MarkdownEditor,
    AdaptiveSpinner,
  },
  emits: ["onCountChanged"],
  setup(_, context) {
    const { apiInterface } = useAPI();
    const { notifier } = useEventHandling();
    const { auth } = useStores();
    const { loading, success, status, data, fetchAPI } = apiInterface();
    const comments = ref([]);
    const commentEditor = ref(null);
    const submitting = ref(false);
    const helpLine = "Please review the guidelines for commenting";
    const model = inject("model");
    const id = inject("id");

    const fetchData = async () => {
      await fetchAPI(requests.comments.getComments(model, id.value));
      if (success.value)
        await commentsSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            comments.value = value.data;
            console.log(comments.value);
            loading.value = false;
          });
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

    onMounted(async () => await fetchData());

    return {
      auth,
      comments,
      loading,
      formatDate,
      commentEditor,
      helpLine,
      onSubmit,
    };
  },
});
</script>
