<template>
  <DetailCard :icon="icon" :no-data="fieldDescription" :title="fieldLabel">
    <template #card-buttons>
      <EditButtons
        v-if="editable"
        @action="editOn = !editOn"
        @cancel="input?.onCancel"
        @remove="onRemove"
        :creating="creating"
        :edit-on="editOn"
        :has-changed="input?.hasChanged"
        :removable="isAttribute && !creating"
        :saving="saving"
        cancellable
      />
    </template>
    <MarkdownEditor
      :ref="`input${uniqueKey}`"
      @on-save-text="onValueChanged"
      :placeholder="placeholder"
      :text="value"
      in-card
    />
  </DetailCard>
</template>

<script>
import { defineComponent, onBeforeMount, provide, useTemplateRef } from "vue";

import { DetailCard, MarkdownEditor } from "@/components";
import { useEditing } from "@/use";
import { isObject, nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "MarkdownField",
  components: {
    DetailCard,
    EditButtons,
    MarkdownEditor,
  },
  props: {
    repository: {
      type: Object,
      required: true,
    },
    id: {
      type: [Number, String],
      required: false,
      default: null,
    },
    field: {
      type: String,
      required: false,
      default: null,
    },
    creating: {
      type: Boolean,
      required: false,
      default: false,
    },
    defaults: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    label: {
      type: String,
      required: false,
      default: "Editor",
    },
    icon: {
      type: String,
      required: false,
      default: "mdi-language-markdown",
    },
    editable: {
      type: Boolean,
      required: false,
      default: true,
    },
    description: {
      type: String,
      required: false,
      default: null,
    },
    placeholder: {
      type: String,
      required: false,
      default: "Type here...",
    },
  },
  setup(props, context) {
    const uniqueKey = crypto.randomUUID();
    const input = useTemplateRef(`input${uniqueKey}`);

    const {
      editOn,
      saving,
      record,
      value,
      loading,
      isAttribute,
      dataField,
      fieldLabel,
      fieldDescription,
      hasChanged,
      onAction,
      onCancel,
      onRemove,
      onValueChanged,
    } = useEditing(props, context, input);

    provide("editOn", editOn);

    onBeforeMount(() => {
      if (!props.creating) {
        record.value = props.repository.find(props.id);
        value.value = record.value[dataField.value];
      } else {
        value.value = "";
      }
    });

    return {
      editOn,
      fieldDescription,
      fieldLabel,
      hasChanged,
      input,
      isAttribute,
      isObject,
      loading,
      nully,
      onAction,
      onCancel,
      saving,
      uniqueKey,
      value,
      onValueChanged,
      onRemove,
    };
  },
});
</script>

<style lang="scss" scoped>
.input-field {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: baseline;
}
.input-field label {
  width: 100%;
}
:deep(.q-field .q-field__control .q-field__append) {
  margin-top: 22px;
}
:deep(.q-field__marginal) {
  height: auto;
}
:deep(.q-icon.text-negative) {
  font-size: 18px;
  width: 23px;
}
:deep(.q-field__bottom) {
  font-size: 11px;
  color: rgb(107 117 175 / 77%);
  padding: 4px 0 0;
}
:deep(.q-field--error .q-field__bottom) {
  color: var(--q-negative);
}
:deep(.no-hint .q-field__bottom) {
  display: none;
}
:deep(.q-field__messages > div) {
  line-height: 1.3;
}
</style>
