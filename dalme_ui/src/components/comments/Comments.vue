<template>
  <q-card class="q-mx-md q-mb-md">
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

    <Spinner :showing="loading" />
  </q-card>
</template>

<script>
import { defineComponent, inject, onMounted, ref } from "vue";

import { requests } from "@/api";
import { CommentForm } from "@/components";
import { Spinner } from "@/components/utils";
import { commentsSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Comments",
  components: {
    CommentForm,
    Spinner,
  },
  setup(_, context) {
    const { loading, success, data, fetchAPI } = useAPI(context);

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
            comments.value = value.results;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return { comments, handleCommented, loading };
  },
});
</script>
