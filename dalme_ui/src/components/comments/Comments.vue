<template>
  <q-card flat class="q-mb-md">
    <q-item class="q-pb-none q-px-sm text-indigo-5">
      <q-item-section side>
        <q-icon name="comment" color="indigo-5" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label class="text-h6">Comments</q-item-label>
      </q-item-section>
    </q-item>
    <q-separator class="bg-indigo-5" />
    <q-card-section v-if="comments.length" class="q-pb-none">
      <div
        v-for="(comment, idx) in comments"
        :key="idx"
        class="comment_threadline q-mt-sm q-pb-lg"
      >
        <q-item class="q-pb-sm q-pt-none q-pr-lg q-pl-none">
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
                <UserPopover v-bind="comment.creationUser" />
                commented
                {{
                  formatDate(
                    comment.creationTimestamp,
                    ["on ", ""],
                    null,
                    (withTime = true),
                  )
                }}
              </q-card-section>
              <q-separator />
              <q-card-section class="text-body2">
                <MarkdownEditor :text="comment.body" />
              </q-card-section>
            </q-card>
          </q-item-section>
        </q-item>
      </div>
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
import { date as qDate } from "quasar";
import { format as timeagoFormat } from "timeago.js";
import MarkdownEditor from "../markdown-editor/MarkdownEditor.vue";

import { requests } from "@/api";
import { CommentForm } from "@/components";
import UserPopover from "../user-popover/UserPopover.vue";
import { Spinner } from "@/components/utils";
import { commentsSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "Comments",
  components: {
    CommentForm,
    MarkdownEditor,
    Spinner,
    UserPopover,
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
            comments.value = value.results;
            loading.value = false;
          });
    };

    const formatDate = (
      string,
      prefixes = null,
      suffixes = null,
      withTime = false,
    ) => {
      let date = null;
      const format = withTime ? "D MMM YYYY @ H:mm" : "D MMM YYYY";
      if (qDate.isValid(string)) {
        if (qDate.getDateDiff(Date.now(), string, "days") > 7) {
          date = qDate.formatDate(string, format);
          if (prefixes) date = `${prefixes[0]}${date}`;
          if (suffixes) date = `${date}${suffixes[0]}`;
        } else {
          date = timeagoFormat(string);
          if (prefixes) date = `${prefixes[1]}${date}`;
          if (suffixes) date = `${date}${suffixes[1]}`;
        }
      }
      return date;
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
