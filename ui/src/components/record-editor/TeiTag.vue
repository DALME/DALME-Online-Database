<template>
  <template v-if="!type.close">
    <div
      :class="`cm-tag-widget ${type.open ? 'open' : 'self-close'} ${section}`"
      @click="showEditor = true"
    >
      <div class="tag-marker">
        <CustomIcon :size="10" :icon="icon" />
        <div class="tag-text" v-if="tagMsg" v-text="tagMsg"></div>
      </div>
      <q-menu class="cm-tag-menu" anchor="center middle" self="center middle">
        <q-card class="q-pa-sm">
          <div>
            <div class="flex no-wrap">
              <div class="column">
                <div class="cm-tag-label items-center row">
                  <CustomIcon :icon="icon" class="q-mr-sm" />
                  <div v-html="`${label}`"></div>
                </div>
                <div class="cm-tag-description" v-html="description"></div>
              </div>
              <div class="cm-tag-remove column items-center q-ml-md">
                <q-btn
                  flat
                  dense
                  v-close-popup
                  color="primary"
                  size="md"
                  icon="mdi-tag-remove"
                  @click="deleteTag"
                />
              </div>
            </div>
            <div class="tag-attributes q-py-sm">
              <template v-for="(attr, index) in attributes" :key="index">
                <div v-if="attr.editable">
                  <template v-if="['string', 'textarea'].includes(attr.kind)">
                    <q-input
                      dense
                      :bottom-slots="!nully(attr.description)"
                      v-model="attr.currentValue"
                      :label="attr.label"
                      :autogrow="attr.kind === 'textarea'"
                      :type="attr.kind === 'string' ? 'text' : 'textarea'"
                      :clearable="!attr.required"
                    >
                      <template v-slot:hint v-if="!nully(attr.description)">
                        <span v-html="attr.description"></span>
                      </template>
                    </q-input>
                  </template>
                  <template v-if="['choice', 'multichoice'].includes(attr.kind)">
                    <q-select
                      dense
                      options-dense
                      map-options
                      :bottom-slots="!nully(attr.description)"
                      v-model="attr.currentValue"
                      :options="attr.options"
                      :multiple="attr.kind === 'multichoice'"
                      :label="attr.label"
                      :clearable="!attr.required"
                    >
                      <template v-slot:hint v-if="!nully(attr.description)">
                        <span v-html="attr.description"></span>
                      </template>
                    </q-select>
                  </template>
                  <template v-if="attr.kind === 'compound'">Stand by...</template>
                </div>
              </template>
            </div>
          </div>
        </q-card>
      </q-menu>
    </div>
  </template>
  <template v-else>
    <div :class="`cm-tag-widget close ${section}`">
      <CustomIcon :size="10" :icon="icon" class="q-mx-auto" />
    </div>
  </template>
</template>

<script>
import { computed, defineComponent, onBeforeUnmount, ref, watch } from "vue";
import { nully } from "@/utils";
import { useSettingsStore } from "@/stores/settings";
import { CustomIcon } from "@/components";

export default defineComponent({
  name: "TeiTag",
  emits: ["update"],
  props: {
    id: {
      type: String,
      required: true,
    },
    tag: {
      type: String,
      required: true,
    },
    attributes: Object,
    type: {
      type: Object,
      required: true,
    },
    from: {
      type: Number,
      required: true,
    },
    to: {
      type: Number,
      required: true,
    },
    section: {
      type: String,
      required: true,
    },
    label: String,
    description: String,
    icon: {
      type: String,
      required: true,
    },
    domEl: {
      type: Object,
      required: true,
    },
  },
  components: {
    CustomIcon,
  },
  setup(props, ctx) {
    const settings = useSettingsStore();
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

    const getAttributeValue = (kind, value) => {
      if (["choice", "multichoice"].includes(kind)) {
        return value.value;
      } else if (kind === "compound") {
        return value;
      } else {
        return value;
      }
    };

    const tagAsText = computed(() => {
      let tag = `<${props.tag}`;
      for (const attr of props.attributes) {
        if (attr.required && !attr.editable) {
          tag += ` ${attr.value}="${attr.default}"`;
        } else if (!nully(attr.currentValue)) {
          tag += ` ${attr.value}="${getAttributeValue(attr.kind, attr.currentValue)}"`;
        }
      }
      tag += ">";
      return tag;
    });

    const deleteTag = () => {
      const changes = [{ from: props.from, to: props.to }];
      // if (pairedEntry) {
      //   changes.push({ from: pairedFrom.value, to: pairedTo.value });
      // }
      ctx.emit("update", changes);
    };

    watch(
      () => props.attributes,
      () => {
        console.log("attributes changed", props.attributes);
        const changes = {
          from: props.from,
          to: props.to,
          insert: tagAsText.value,
        };
        ctx.emit("update", changes);
      },
      { deep: true },
    );

    onBeforeUnmount(() => {
      props.domEl.removeAttribute("id");
    });

    return {
      showEditor,
      nully,
      deleteTag,
      settings,
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
