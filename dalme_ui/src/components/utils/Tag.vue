<template>
  <q-icon v-if="mini" :name="miniIcon" :color="tagColours.text" :size="size" />
  <q-badge
    v-else
    :color="tagColours.colour"
    :text-color="tagColours.text"
    :class="`tag-${size}`"
    :label="name"
  />
</template>

<script>
import { computed, defineComponent } from "vue";
import { useConstantStore } from "@/stores/constants";

export default defineComponent({
  name: "Tag",
  props: {
    colour: {
      type: String,
      required: false,
    },
    name: {
      type: String,
      required: false,
    },
    mini: {
      type: Boolean,
      required: false,
      default: false,
    },
    module: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      required: false,
      default: "sm",
    },
    textColour: {
      type: String,
      required: false,
    },
    type: {
      type: String,
      required: false,
    },
    wfStage: {
      type: Number,
      required: false,
    },
    wfStatus: {
      type: Number,
      required: false,
    },
  },
  setup(props) {
    const $constantStore = useConstantStore();
    const converter =
      props.module === "workflow"
        ? $constantStore.workflowTagColours
        : $constantStore.ticketTagColours;

    const tagColours = computed(() =>
      props.module === "standalone"
        ? { colour: props.colour, text: props.textColour }
        : converter[props.type],
    );

    const miniIcon = computed(() => {
      if (props.module === "workflow") {
        if (props.wfStatus === 2) {
          return $constantStore.workflowIconbyStage[props.wfStage];
        } else {
          return $constantStore.workflowIconbyStatus[props.wfStatus];
        }
      } else {
        return $constantStore.ticketTagIcon[props.type];
      }
    });

    return { miniIcon, tagColours };
  },
});
</script>

<style lang="scss">
.tag-sm {
  border: 1px solid;
  text-transform: uppercase;
  font-size: 10px;
  font-weight: 600;
}
.tag-xs {
  border: 1px solid;
  text-transform: uppercase;
  font-size: 8px;
  font-weight: 600;
  height: 14px;
  padding: 0px 4px;
}
</style>
