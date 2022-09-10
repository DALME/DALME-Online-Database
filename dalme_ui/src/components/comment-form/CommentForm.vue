<template>
  <q-item class="q-py-sm q-pr-lg q-pl-none">
    <q-item-section top avatar>
      <q-avatar v-if="authStore.avatar" size="40px">
        <img :src="authStore.avatar" />
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
        ref="commentForm"
        editable
        placeholder="Leave a comment..."
        :help="helpLine"
        submitLabel="Comment"
        @on-save-text="onSubmit"
      />
    </q-item-section>
  </q-item>
</template>

<script>
// import { openURL } from "quasar";
import { defineComponent, inject, ref } from "vue";
import { useAuthStore } from "@/stores/auth";

import { requests } from "@/api";
import { commentPayloadSchema, commentSchema } from "@/schemas";
import { useAPI, useNotifier } from "@/use";
import MarkdownEditor from "../markdown-editor/MarkdownEditor.vue";

export default defineComponent({
  name: "CommentForm",
  components: { MarkdownEditor },
  emits: ["onSubmitComment"],
  setup(_, context) {
    const { apiInterface } = useAPI();
    const $notifier = useNotifier();
    const authStore = useAuthStore();

    const { data, fetchAPI, status } = apiInterface();
    const commentForm = ref("");
    const submitting = ref(false);
    const helpLine = "Please review the guidelines for commenting";

    const model = inject("model");
    const id = inject("id");

    // const openKB = () => {
    //   openURL("https://kb.dalme.org/", null, { target: "_blank" });
    // };

    const onSubmit = async (text) => {
      submitting.value = true;
      const payload = { model, body: text, object: id.value };
      await commentPayloadSchema.validate(payload);
      setTimeout(async () => {
        const request = requests.comments.addComment(payload);
        await fetchAPI(request);
        /* eslint-disable */
        status.value == 201
          ? commentSchema.validate(data.value).then(() => {
              commentForm.value.resetEditor();
              $notifier.comments.commentAdded();
              context.emit("onSubmitComment");
            })
          : $notifier.comments.commentFailed();
        /* eslint-enable */
      }, 250);
      submitting.value = false;
    };

    return {
      authStore,
      commentForm,
      helpLine,
      onSubmit,
    };
  },
});
</script>
