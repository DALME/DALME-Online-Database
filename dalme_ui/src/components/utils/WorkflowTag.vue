<template>
  <q-badge
    :color="tagColours.colour"
    :text-color="tagColours.text"
    class="wf-tag"
  >
    {{ status.titleText }}
  </q-badge>
</template>

<script>
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "WorkflowTag",
  props: {
    status: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const getTagColours = (tag) => {
      if (tag === "tag-wf-awaiting")
        return { colour: "deep-purple-1", text: "deep-purple-8" };

      if (tag === "tag-wf-in_progress")
        return { colour: "blue-1", text: "blue-9" };

      if (tag === "tag-wf-assessing")
        return { colour: "orange-1", text: "orange-9" };

      if (tag === "tag-wf-processed")
        return { colour: "green-1", text: "green-10" };

      if (tag === "tag-wf-unknown") return { colour: "red-1", text: "red-10" };
    };

    const tagColours = computed(() => getTagColours(props.status.cssClass));

    return { tagColours };
  },
});
</script>
