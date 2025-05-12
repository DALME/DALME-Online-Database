<template>
  <div v-if="!loading" class="input-field">
    <q-input
      :ref="`input${uniqueKey}`"
      v-model="value"
      :class="showBottom ? '' : 'no-hint'"
      :hint="fieldDescription"
      :label="fieldLabel"
      :placeholder="placeholder"
      :readonly="!editOn"
      :rules="[validate]"
      color="indigo-8"
      debounce="500"
      autogrow
      hide-bottom-space
      stack-label
    >
      <template #append>
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          @navigate="router.push(link)"
          @remove="onRemove"
          :creating="creating"
          :edit-on="editOn"
          :has-changed="hasChanged"
          :linkable="isObject(link)"
          :removable="isAttribute && !creating"
          :saving="saving"
          cancellable
        />
      </template>
    </q-input>
  </div>
</template>

<script>
import { defineComponent, onBeforeMount, onMounted, useTemplateRef } from "vue";
import { useRouter } from "vue-router";

import { useEditing } from "@/use";
import { isObject, nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "InputField",
  components: { EditButtons },
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
      default: "Input",
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
    link: {
      type: Object,
      required: false,
      default: null,
    },
    placeholder: {
      type: String,
      required: false,
      default: "Type value here...",
    },
  },
  emits: ["drop", "created", "destroyed"],
  setup(props, context) {
    const uniqueKey = crypto.randomUUID();
    const input = useTemplateRef(`input${uniqueKey}`);
    const router = useRouter();

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
      showBottom,
      onAction,
      onCancel,
      onRemove,
      validate,
    } = useEditing(props, context, input);

    onBeforeMount(() => {
      record.value = props.creating ? props.defaults : props.repository.find(props.id);
      value.value = props.creating ? "" : record.value[dataField.value];
    });

    onMounted(() => {
      if (props.creating) {
        input.value.focus();
        editOn.value = true;
      }
    });

    return {
      editOn,
      fieldDescription,
      fieldLabel,
      hasChanged,
      isAttribute,
      isObject,
      loading,
      nully,
      onAction,
      onCancel,
      router,
      saving,
      showBottom,
      uniqueKey,
      validate,
      value,
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
:deep(.q-field textarea.q-field__native) {
  align-content: center;
  padding: 0;
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
