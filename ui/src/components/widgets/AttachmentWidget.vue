<template>
  <template v-if="compact">
    <q-icon :name="icon" :style="iconStyle" :color="color">
      <ToolTip v-if="iconOnly">{{ attachment.filename }}</ToolTip>
    </q-icon>
    <ExternalLink
      v-if="!iconOnly"
      :url="attachment.source"
      :title="attachment.filename"
      inline
      class="q-ml-xs"
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
          <template v-slot:loading>
            <q-spinner />
          </template>
          <template v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              Couldn't load attachment
            </div>
          </template>
          <div class="absolute-bottom-right text-subtitle1 text-center">
            <a :href="attachment.source" target="_blank" class="q-pa-sm text-white">
              {{ attachment.filename }}
            </a>
          </div>
        </q-img>
      </q-card-section>
      <AdaptiveSpinner :showing="!attachment" />
    </q-card>
  </template>
</template>

<script>
import { computed, defineComponent, defineAsyncComponent, inject } from "vue";
import { useConstants } from "@/use";
import { AdaptiveSpinner, ExternalLink } from "@/components";

export default defineComponent({
  name: "AttachmentWidget",
  props: {
    file: Object,
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
  components: {
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
    AdaptiveSpinner,
    ExternalLink,
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
