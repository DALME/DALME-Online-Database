<template>
  <q-icon v-if="mini" :name="miniIcon" :color="tagColours.text" :size="size" />
  <q-badge
    v-else
    :color="outline ? 'transparent' : tagColours.colour"
    :text-color="tagColours.text"
    :class="`tag-${size}`"
    :label="name"
  />
</template>

<script>
import { computed, defineComponent } from "vue";
import { useConstants } from "@/use";

export default defineComponent({
  name: "TagWidget",
  props: {
    colour: {
      type: String,
      required: false,
    },
    name: {
      type: [String, Number],
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
    outline: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const {
      ticketTagColours,
      ticketTagIcon,
      workflowTagColours,
      workflowIconbyStage,
      workflowIconbyStatus,
    } = useConstants();

    const converter = props.module === "workflow" ? workflowTagColours : ticketTagColours;

    // const tagColours = computed(() =>
    //   props.module === "standalone"
    //     ? { colour: props.colour, text: props.textColour }
    //     : converter[props.type],
    // );

    // TODO: fix this horrible hack (this was a quick solution after changing models)
    const tagColours = computed(() => {
      if (props.module === "workflow") {
        let type = props.type;
        type = ["ingestion", "transcription", "markup", "review", "parsing"].reduce(
          (result, word) => result.replace(word, ""),
          type,
        );
        type = type.trim().replace(" ", "_");
        return converter[type];
      } else if (props.module === "standalone") {
        return { colour: props.colour, text: props.textColour };
      } else {
        return converter[props.type];
      }
    });

    const miniIcon = computed(() => {
      if (props.module === "workflow") {
        if (props.wfStatus === 2) {
          return workflowIconbyStage[props.wfStage];
        } else {
          return workflowIconbyStatus[props.wfStatus];
        }
      } else {
        return ticketTagIcon[props.type];
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
.transparent {
  background: none;
}
</style>
