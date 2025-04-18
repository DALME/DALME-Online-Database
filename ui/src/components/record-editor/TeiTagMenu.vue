<template>
  <q-menu anchor="center middle" class="cm-tag-menu" self="center middle">
    <q-card class="q-pa-sm">
      <div>
        <div class="flex no-wrap">
          <div class="column">
            <div class="cm-tag-label items-center row">
              <CustomIcon :icon="icon" class="q-mr-sm" />
              <div v-html="`${elData.label}`"></div>
            </div>
            <div v-html="elData.description" class="cm-tag-description"></div>
          </div>
          <div v-if="action == 'edit'" class="cm-tag-remove column items-center q-ml-md">
            <q-btn
              v-close-popup
              @click="deleteTag"
              color="primary"
              icon="mdi-tag-remove"
              size="md"
              dense
              flat
            />
          </div>
        </div>
        <div class="tag-attributes q-py-sm">
          <template v-for="(attr, index) in data" :key="index">
            <div v-if="attr.editable">
              <template v-if="['string', 'textarea'].includes(attr.kind)">
                <q-input
                  v-model="attr.currentValue"
                  :autogrow="attr.kind === 'textarea'"
                  :bottom-slots="!nully(attr.description)"
                  :clearable="!attr.required"
                  :label="attr.label"
                  :type="attr.kind === 'string' ? 'text' : 'textarea'"
                  dense
                >
                  <template #hint v-if="!nully(attr.description)">
                    <span v-html="attr.description"></span>
                  </template>
                </q-input>
              </template>
              <template v-if="['choice', 'multichoice'].includes(attr.kind)">
                <q-select
                  v-model="attr.currentValue"
                  :bottom-slots="!nully(attr.description)"
                  :clearable="!attr.required"
                  :label="attr.label"
                  :multiple="attr.kind === 'multichoice'"
                  :options="attr.options"
                  dense
                  map-options
                  options-dense
                >
                  <template #hint v-if="!nully(attr.description)">
                    <span v-html="attr.description"></span>
                  </template>
                </q-select>
              </template>
              <template v-if="attr.kind === 'compound'">Stand by...</template>
            </div>
          </template>
        </div>
        <q-btn
          v-if="action === 'create'"
          @click="insertTag"
          class="editor-tb-button"
          label="Insert"
          size="xs"
          flat
        />
      </div>
    </q-card>
  </q-menu>
</template>

<script>
import { groupBy, prop, filter as rFilter } from "ramda";
import { computed, defineComponent, onMounted, ref, watch } from "vue";

import { CustomIcon } from "@/components";
import { useSettingsStore } from "@/stores/settings";
import { nully } from "@/utils";

export default defineComponent({
  name: "TeiTagMenu",
  components: {
    CustomIcon,
  },
  props: {
    tagData: {
      type: Object,
      required: true,
    },
    elData: {
      type: Object,
      required: true,
    },
    attributes: {
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
    action: {
      type: String,
      default: "edit",
    },
  },
  emits: ["update", "insert"],
  setup(props, ctx) {
    const settings = useSettingsStore();
    const isCompound = props.elData.compound;
    const icon = props.tagData.icon || props.elData.icon;
    const data = ref({});

    const tagAsText = computed(() => {
      let tag = `<${props.tagData.name}`;
      const attributes = isCompound ? rFilter((x) => x.group === props.tagData.name) : data.value;
      for (const attr of attributes) {
        if (attr.required && !attr.editable) {
          tag += ` ${attr.value}="${attr.default}"`;
        } else if (!nully(attr.currentValue)) {
          const val = ["choice", "multichoice"].includes(attr.kind)
            ? attr.currentValue.value
            : attr.currentValue;
          tag += ` ${attr.value}="${val}"`;
        }
      }
      tag += ">";
      return tag;
    });

    const deleteTag = () => {
      ctx.emit("update", { from: props.from, to: props.to });
    };

    const insertTag = () => {
      ctx.emit("insert", groupBy(prop("group"), data.value));
    };

    const generateTagAttributes = (refAttrs, localAttrs, kind, action, group) => {
      // console.log("generating from", refAttrs);
      const result = [];
      for (const attr of refAttrs) {
        if (action !== "create" && kind === "supplied" && attr.value === "text") {
          continue;
        } else {
          let cValue;
          if (localAttrs && attr.value in localAttrs) {
            cValue = structuredClone(localAttrs[attr.value]);
          } else if (attr.default) {
            cValue = structuredClone(attr.default);
          } else {
            cValue = attr.kind === "multichoice" ? [] : "";
          }
          result.push({
            group: group,
            default: attr.label || null,
            description: attr.description,
            editable: attr.editable,
            required: attr.required,
            kind: attr.kind,
            label: attr.label,
            value: attr.value,
            options: attr.options || [],
            currentValue: cValue,
          });
        }
      }
      // console.log("result = ", result);
      return result;
    };

    const generateData = () => {
      let result = generateTagAttributes(
        props.tagData.attributes,
        props.attributes,
        props.tagData.kind,
        props.action,
        props.tagData.name,
      );
      if (props.action === "create" && props.elData.label === "Gloss") {
        // console.log("og result", data.value);
      }
      if (props.action === "create" && isCompound) {
        for (const tag of props.elData.tags) {
          if (tag.attributes.length) {
            result = result.concat(
              generateTagAttributes(tag.attributes, null, tag.kind, props.action, tag.name),
            );
          }
        }
      }
      if (props.action === "create" && props.elData.label === "Gloss") {
        // console.log("final result", data.value);
      }
      return result;
    };

    onMounted(() => {
      data.value = generateData();
      if (props.action === "create" && props.elData.label === "Gloss") {
        // console.log("data", data.value);
      }

      if (props.action === "edit") {
        watch(
          () => data.value,
          () => {
            // console.log("data updated");
            ctx.emit("update", {
              from: props.from,
              to: props.to,
              insert: tagAsText.value,
            });
          },
          { deep: true },
        );
      }
    });

    return {
      nully,
      deleteTag,
      insertTag,
      settings,
      icon,
      data,
    };
  },
});
</script>

<style lang="scss" scoped>
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
