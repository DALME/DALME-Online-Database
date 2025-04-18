<template>
  <template v-if="compact">
    <q-icon :color="color" :name="icon" :style="iconStyle">
      <ToolTip v-if="iconOnly">{{ attachment.filename }}</ToolTip>
    </q-icon>
    <ExternalLink
      v-if="!iconOnly"
      :title="attachment.filename"
      :url="attachment.source"
      class="q-ml-xs"
      inline
    />
  </template>
  <template v-else>
    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar icon="attachment" />
        </q-item-section>
        <q-item-section>
          <q-item-label class="text-subtitle1">Attachments</q-item-label>
        </q-item-section>
      </q-item>
      <q-card-section>
        <q-img :src="attachment.source">
          <template #loading>
            <q-spinner />
          </template>
          <template #error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              Couldn't load attachment
            </div>
          </template>
          <div class="absolute-bottom-right text-subtitle1 text-center">
            <a :href="attachment.source" class="q-pa-sm text-white" target="_blank">
              {{ attachment.filename }}
            </a>
          </div>
        </q-img>
      </q-card-section>
      <AdaptiveSpinner :showing="!attachment" class="q-ma-auto" />
    </q-card>
  </template>
</template>

<script>
import { computed, defineAsyncComponent, defineComponent, inject } from "vue";

import { AdaptiveSpinner, ExternalLink } from "@/components";
import { useConstants } from "@/use";

export default defineComponent({
  name: "AttachmentWidget",
  components: {
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
    AdaptiveSpinner,
    ExternalLink,
  },
  props: {
    file: {
      type: Object,
      required: false,
      default: null,
    },
    iconOnly: {
      type: Boolean,
      default: false,
    },
    compact: {
      type: Boolean,
      default: false,
    },
    preview: {
      type: Boolean,
      default: true,
    },
    size: {
      type: String,
      default: "18px",
    },
    color: {
      type: String,
      default: "currentColor",
    },
  },

  setup(props) {
    const attachment = props.file ? props.file : inject("attachment");
    const { attachmentIcons } = useConstants();
    const icon = computed(() =>
      props.file.filetype in attachmentIcons ? attachmentIcons[props.file.filetype] : "mdi-file",
    );
    const iconStyle = computed(() =>
      props.iconOnly ? "width: 23px;" : `font-size: ${props.size};`,
    );

    return {
      attachment,
      icon,
      iconStyle,
    };
  },
});
</script>
