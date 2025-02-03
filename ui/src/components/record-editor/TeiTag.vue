<template>
  <div
    :class="`cm-tag-widget ${type === 'OpenTag' ? 'open' : 'self-close'} ${section}`"
    @click="showEditor = true"
  >
    <div class="tag-marker">
      <CustomIcon :size="10" :icon="icon" />
      <div class="tag-text" v-if="tagMsg" v-text="tagMsg"></div>
    </div>
    <TeiTagMenu
      :tag="tag"
      :attributes="attributes"
      :icon="icon"
      :label="label"
      :description="description"
    />
  </div>
</template>

<script>
import { computed, defineComponent, onBeforeUnmount, ref } from "vue";
import { nully } from "@/utils";
import { CustomIcon } from "@/components";
import TeiTagMenu from "./TeiTagMenu.vue";

export default defineComponent({
  name: "TeiTag",
  emits: ["update"],
  props: {
    id: String,
    widgetId: String,
    tag: String,
    attributes: Object,
    type: String,
    from: Number,
    to: Number,
    section: String,
    label: String,
    description: String,
    icon: String,
    domEl: Object,
  },
  components: {
    CustomIcon,
    TeiTagMenu,
  },
  setup(props) {
    const showEditor = ref(false);
    const msgAttrs = ["xml:id", "target", "columns", "n"];
    const tagMsg = computed(() => {
      if (props.tag === "table") {
        const rows = props.attributes.find((attr) => attr.value === "rows").currentValue;
        const cols = props.attributes.find((attr) => attr.value === "cols").currentValue;
        return `${rows}x${cols}`;
      } else if (props.tag === "row") {
        if (props.attributes.find((attr) => attr.value === "role").currentValue === "label") {
          return "H";
        }
      } else if (props.tag === "num") {
        return props.attributes.find((attr) => attr.value === "value").currentValue;
      } else if (props.tag === "g") {
        console.log("glyph", props.attributes.find((attr) => attr.value === "ref").currentValue);
        return String.fromCodePoint(
          `0x${props.attributes.find((attr) => attr.value === "ref").currentValue}`,
        );
      } else {
        for (const attr of msgAttrs) {
          if (props.attributes.find((x) => x.value === attr)) {
            return props.attributes.find((x) => x.value === attr).currentValue;
          }
        }
      }
      return null;
    });

    onBeforeUnmount(() => {
      console.log("component destroyed:", props.id);
      props.domEl.removeAttribute("id");
    });

    return {
      showEditor,
      nully,
      tagMsg,
    };
  },
});
</script>

<style lang="scss">
.cm-tag-widget-container {
  display: inline-block;
  margin: 0 5px;
  vertical-align: middle;
}
// .cm-widgetBuffer:first-child + .cm-tag-widget-container {
//   margin-left: 0;
// }
.cm-tag-widget {
  border: 2px solid rgb(171 178 191);
  border-radius: 6px;
  height: 20px;
  min-width: 22px;
  display: flex;
  align-items: center;
}
.cm-tag-widget .tag-marker {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding-left: 2px;
  padding-right: 2px;
}
.cm-tag-widget .tag-marker .tag-text {
  font-size: 10px;
  font-family: "Roboto";
  font-weight: 400;
}
.cm-tag-widget.open {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right: none;
}
.cm-tag-widget.close {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-left: none;
}
.cm-tag-widget.close i {
  font-size: 10px;
}
.cm-tag-widget.annotation {
  border-color: #684545;
  color: #b08181;
  // background-color: #342828;
}
.cm-tag-widget.editorial {
  border-color: #3c7072;
  color: #749ba5;
  // background-color: #253335;
}
.cm-tag-widget.formatting {
  border-color: #4b6391;
  color: #9eb5e7;
  // background-color: #2b343b;
}
.cm-tag-widget.layout {
  border-color: #3d7746;
  color: #71b572;
  // background-color: #273124;
}
.cm-tag-widget.marks {
  border-color: #704b91;
  color: #9e73ae;
  // background-color: #362b3b;
}
.cm-tag-widget.other {
  border-color: #615f5f;
  color: #9c9797;
  // background-color: #2d2c2c;
}
.cm-tag-widget.self-close:hover,
.cm-tag-widget.open:hover {
  // background-color: #ffffff1a;
  border-color: #ffffffc9;
  color: #e7e3e3;
}
.cm-tag-menu {
  max-width: 300px;
}
.cm-tag-label div {
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 600;
}
.cm-tag-description {
  font-size: 11px;
  color: rgba(0, 0, 0, 0.54);
}
.q-field__append.q-field__marginal .q-icon {
  font-size: 18px;
}
</style>
