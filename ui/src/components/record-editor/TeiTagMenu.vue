<template>
  <q-menu
    ref="tag-menu"
    :persistent="persistent"
    anchor="center middle"
    class="cm-tag-menu"
    self="center middle"
  >
    <q-card class="q-pa-sm">
      <div>
        <div class="flex no-wrap items-center">
          <CustomIcon :icon="icon" :size="20" class="tag-menu-icon" />
          <div class="column">
            <div class="cm-tag-label items-center row">
              <div v-html="`${elData.label}`"></div>
            </div>
            <div v-html="elData.description" class="cm-tag-description"></div>
          </div>
          <div v-if="action == 'edit'" class="cm-tag-remove column items-center q-ml-md">
            <q-btn
              v-close-popup
              @click="deleteTag"
              class="delete-tag-button"
              color="blue-grey-5"
              icon="mdi-trash-can-outline"
              size="md"
              dense
              flat
              round
            >
              <ToolTip>Delete this tag.</ToolTip>
            </q-btn>
          </div>
        </div>
        <div class="tag-attributes q-py-md">
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
                  class="tag-field"
                  standout="bg-blue-grey text-white"
                  dense
                >
                  <template #hint v-if="!nully(attr.description)">
                    <span v-html="attr.description" class="ellipsis"></span>
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
                  class="tag-field"
                  standout="bg-blue-grey text-white"
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
        <div class="button-container">
          <q-btn
            @click="cancelTag"
            :color="buttonDisabled ? 'grey-5' : 'blue-grey-7'"
            :disable="buttonDisabled"
            :label="cancelButtonLabel"
            class="tag-menu-button q-mr-sm"
            dense
            outline
          />
          <q-btn
            @click="saveTag"
            :color="buttonDisabled ? 'grey-5' : 'light-green-9'"
            :disable="buttonDisabled"
            :label="okButtonLabel"
            class="tag-menu-button"
            dense
            outline
          />
        </div>
      </div>
    </q-card>
  </q-menu>
</template>

<script>
import { groupBy, prop, filter as rFilter } from "ramda";
import { computed, defineComponent, onMounted, ref, useTemplateRef, watch } from "vue";

import { CustomIcon, ToolTip } from "@/components";
import { useSettingsStore } from "@/stores/settings";
import { nully } from "@/utils";

export default defineComponent({
  name: "TeiTagMenu",
  components: {
    CustomIcon,
    ToolTip,
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
      default: null,
    },
    from: {
      type: Number,
      default: null,
    },
    to: {
      type: Number,
      default: null,
    },
    action: {
      type: String,
      default: "edit",
    },
  },
  emits: ["update", "insert"],
  setup(props, ctx) {
    const settings = useSettingsStore();
    const menu = useTemplateRef("tag-menu");
    const isCompound = props.elData.compound;
    const icon = props.tagData.icon || props.elData.icon;
    const data = ref({});
    const hasChanged = ref(false);

    const okButtonLabel = computed(() => (props.action === "create" ? "Insert" : "Save"));
    const cancelButtonLabel = computed(() => (props.action === "create" ? "Cancel" : "Revert"));
    const buttonDisabled = computed(() => props.action === "edit" && !hasChanged.value);
    const persistent = computed(() => props.action === "edit" && hasChanged.value);

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

    const saveTag = () => {
      if (props.action === "create") {
        ctx.emit("insert", groupBy(prop("group"), data.value));
      } else {
        ctx.emit("update", {
          from: props.from,
          to: props.to,
          insert: tagAsText.value,
        });
      }
    };

    const cancelTag = () => {
      if (props.action === "create") {
        menu.value.hide();
      } else {
        generateData().then(() => (hasChanged.value = false));
      }
    };

    const deleteTag = () => {
      ctx.emit("update", { from: props.from, to: props.to });
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
      return new Promise((resolve) => {
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
        data.value = result;
        resolve();
      });
    };

    onMounted(() => {
      generateData();
      if (props.action === "create" && props.elData.label === "Gloss") {
        // console.log("data", data.value);
      }

      watch(
        () => data.value,
        () => (hasChanged.value = true),
        { deep: true },
      );
    });

    return {
      nully,
      deleteTag,
      saveTag,
      cancelTag,
      settings,
      icon,
      data,
      okButtonLabel,
      cancelButtonLabel,
      buttonDisabled,
      persistent,
    };
  },
});
</script>

<style lang="scss" scoped>
.cm-tag-label div {
  font-size: 13px;
  text-transform: uppercase;
  font-weight: 900;
  line-height: 1.2;
  letter-spacing: 0.05em;
  color: #4d6584;
}
.cm-tag-description {
  font-size: 11px;
  color: rgba(0, 0, 0, 0.54);
  max-width: 190px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
.q-field__append.q-field__marginal .q-icon {
  font-size: 18px;
}
.tag-menu-button {
  font-size: 11px;
  font-weight: 900;
  padding: 2px 12px;
}
.tag-menu-button::after {
  content: "";
  position: absolute;
  background: currentColor !important;
  opacity: 0.05;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  border-radius: 4px;
}
.delete-tag-button {
  border: 1px dotted rgba(0, 0, 0, 0.2);
}
.delete-tag-button:hover {
  color: #ff5722 !important;
}
:deep(.tag-field .q-field__append .q-icon) {
  font-size: 16px;
}
.button-container {
  display: flex;
  align-items: center;
  justify-content: end;
}
.tag-menu-icon {
  border-radius: 3px;
  padding: 6px;
  align-self: center;
  background-color: #d7dfe3;
  color: #4d6584;
  margin-right: 10px;
}
.q-field__messages span.ellipsis {
  display: block;
  max-width: 290px;
}
</style>
