<template>
  <q-card class="q-ma-md">
    <q-item>
      <q-item-section avatar>
        <q-avatar icon="comment"> </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label class="text-subtitle1">Comments</q-item-label>
      </q-item-section>
    </q-item>

    <q-card-section v-if="comments.length">
      <q-card v-for="(comment, idx) in comments" :key="idx" class="q-mb-md">
        <q-item>
          <q-item-section avatar>
            <q-avatar>
              <img :src="comment.creationUser.avatar" />
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label>
              <router-link
                :to="{
                  name: 'User',
                  params: { username: comment.creationUser.username },
                }"
              >
                {{ comment.creationUser.fullName }}
              </router-link>
            </q-item-label>
            <q-item-label caption>
              Commented on {{ comment.creationTimestamp }}
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-card-section v-html="comment.body"> </q-card-section>
      </q-card>
    </q-card-section>

    <q-separator />

    <q-card-section>
      <CommentForm @on-submit-comment="handleCommented" />
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, inject, ref } from "vue";

import { requests } from "@/api";
import { CommentForm } from "@/components";
import { commentsSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Comments",
  components: {
    CommentForm,
  },
  async setup() {
    const { success, data, fetchAPI } = useAPI();

    const comments = ref([]);

    const model = inject("model");
    const objId = inject("objId");

    const handleCommented = async () => {
      await fetchComments();
    };

    const fetchComments = async () => {
      await fetchAPI(requests.comments.getComments(model, objId.value));
      if (success.value)
        await commentsSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            comments.value = value.results;
          });
    };

    await fetchComments();

    return { comments, handleCommented };
  },
});
</script>
