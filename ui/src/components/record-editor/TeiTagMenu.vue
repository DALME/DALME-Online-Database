<template>
  <q-menu class="cm-tag-menu" anchor="center middle" self="center middle">
    <q-card class="q-pa-sm">
      <div>
        <div class="flex no-wrap">
          <div class="column">
            <div class="cm-tag-label items-center row">
              <CustomIcon :icon="icon" class="q-mr-sm" />
              <div v-html="`${elData.label}`"></div>
            </div>
            <div class="cm-tag-description" v-html="elData.description"></div>
          </div>
          <div v-if="action == 'edit'" class="cm-tag-remove column items-center q-ml-md">
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
          <template v-for="(attr, index) in data" :key="index">
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
        <q-btn
          v-if="action === 'create'"
          flat
          size="xs"
          label="Insert"
          class="editor-tb-button"
          @click="insertTag"
        />
      </div>
    </q-card>
  </q-menu>
</template>

<script>
import { computed, defineComponent, onMounted, ref, watch } from "vue";
import { nully } from "@/utils";
import { useSettingsStore } from "@/stores/settings";
import { CustomIcon } from "@/components";
import { filter as rFilter, groupBy, prop } from "ramda";

export default defineComponent({
  name: "TeiTagMenu",
  emits: ["update", "insert"],
  props: {
    tagData: {
      type: Object,
      required: true,
    },
    elData: {
      type: Object,
      required: true,
    },
    attributes: Object,
    label: String,
    description: String,
    from: Number,
    to: Number,
    action: {
      type: String,
      default: "edit",
    },
  },
  components: {
    CustomIcon,
  },
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
