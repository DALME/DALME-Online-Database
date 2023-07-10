<template>
  <q-icon :name="icon" class="attachment-icon">
    <TooltipWidget>{{ attachment.filename }}</TooltipWidget>
  </q-icon>
</template>

<script>
import { computed, defineComponent, defineAsyncComponent } from "vue";
import { useConstants } from "@/use";

export default defineComponent({
  name: "AttachmentIconWidget",
  props: {
    attachment: {
      type: Object,
      required: true,
    },
  },
  components: {
    TooltipWidget: defineAsyncComponent(() => import("@/components/widgets/TooltipWidget.vue")),
  },
  setup(props) {
    const { attachmentIcons } = useConstants();
    const icon = computed(() =>
      props.attachment.filetype in attachmentIcons
        ? attachmentIcons[props.attachment.filetype]
        : "mdi-file",
    );

    return { icon };
  },
});
</script>

<style lang="scss">
.attachment-icon {
  width: 23px;
}
</style>
