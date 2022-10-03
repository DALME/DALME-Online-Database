<template>
  <q-card flat>
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
              <q-card-section class="bg-grey-2 q-py-sm">
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
      <CommentForm @on-submit-comment="handleCommented" />
    </q-card-section>
    <Spinner :showing="loading" />
  </q-card>
</template>

<script>
import { defineComponent, inject, onMounted, ref } from "vue";
import MarkdownEditor from "../markdown-editor/MarkdownEditor.vue";

import { requests } from "@/api";
import { CommentForm } from "@/components";
import { DetailPopover } from "@/components/utils";
import { formatDate, Spinner } from "@/components/utils";
import { commentsSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Comments",
  components: {
    CommentForm,
    DetailPopover,
    MarkdownEditor,
    Spinner,
  },
  setup() {
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const comments = ref([]);

    const model = inject("model");
    const id = inject("id");

    const handleCommented = async () => {
      await fetchData();
    };

    const fetchData = async () => {
      await fetchAPI(requests.comments.getComments(model, id.value));
      if (success.value)
        await commentsSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            comments.value = value.data;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return {
      comments,
      handleCommented,
      loading,
      formatDate,
    };
  },
});
</script>

<style lang="scss" scoped>
.comment_threadline {
  background: linear-gradient(#e0e0e0, #e0e0e0) no-repeat 70px/2px 100%;
}
</style>
