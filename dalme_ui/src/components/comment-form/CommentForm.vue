<template>
  <q-form
    @submit="onSubmit"
    ref="commentForm"
    autocapitalize="off"
    autocomplete="off"
    autocorrect="off"
  >
    <q-input
      v-model="body"
      name="body"
      :label="label"
      autogrow
      clearable
      filled
    />
    <div class="row">
      <q-space />
      <q-btn
        label="Submit"
        type="submit"
        color="primary"
        class="q-mt-md"
        :disable="disabled"
      />
    </div>
  </q-form>
</template>

<script>
import { isEmpty } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";

import { requests } from "@/api";
import notifier from "@/notifier";
import { commentPayloadSchema, commentSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "CommentForm",
  emits: ["onSubmitComment"],
  setup(_, { emit }) {
    const { data, fetchAPI, status } = useAPI();

    const body = ref("");
    const commentForm = ref("");
    const submitting = ref(false);
    const disabled = computed(() => isEmpty(body.value));
    const label = "Leave a comment...";

    const model = inject("model");
    const objId = inject("objId");

    const onSubmit = async () => {
      submitting.value = true;
      const payload = { model, body: body.value, object: objId.value };
      await commentPayloadSchema.validate(payload);
      setTimeout(async () => {
        const request = requests.comments.addComment(payload);
        await fetchAPI(request);
        /* eslint-disable */
        status.value == 201
          ? commentSchema.validate(data.value).then(() => {
              body.value = "";
              commentForm.value.resetValidation();
              notifier.comments.commentAdded();
              emit("onSubmitComment");
            })
          : notifier.comments.commentFailed();
        /* eslint-enable */
      }, 250);
      submitting.value = false;
    };
    return { body, commentForm, disabled, label, onSubmit };
  },
});
</script>
