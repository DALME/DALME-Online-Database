<template>
  <div v-if="!loading" class="boolean-field">
    <q-field
      :borderless="!editOn"
      :class="fieldDescription ? '' : 'no-hint'"
      :hint="fieldDescription"
      :readonly="!editOn"
      hide-bottom-space
    >
      <q-checkbox
        v-model="value"
        :disable="!editOn"
        :label="fieldLabel"
        checked-icon="task_alt"
        unchecked-icon="highlight_off"
        dense
        left-label
      />
      <template #append>
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          @remove="onRemove"
          :creating="creating"
          :edit-on="editOn"
          :has-changed="hasChanged"
          :removable="isAttribute && !creating"
          :saving="saving"
          cancellable
        />
      </template>
    </q-field>
  </div>
</template>

<script>
import { defineComponent, onBeforeMount } from "vue";
import { useRouter } from "vue-router";

import { useEditing } from "@/use";
import { isObject, nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "BooleanField",
  components: { EditButtons },
  props: {
    repository: {
      type: Object,
      required: true,
    },
    id: {
      type: [Number, String],
      required: true,
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
      default: "Checkbox",
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
  },
  emits: ["drop", "created", "destroyed"],

  setup(props, context) {
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
      onAction,
      onCancel,
      onRemove,
    } = useEditing(props, context);

    onBeforeMount(() => {
      record.value = props.repository.find(props.id);
      value.value = record.value[dataField.value];
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
      value,
      onRemove,
    };
  },
});
</script>

<style lang="scss" scoped>
.boolean-field {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: baseline;
}
.boolean-field label {
  width: 100%;
}
.q-field .q-checkbox {
  height: 32px;
  align-self: anchor-center;
}
:deep(.q-field .q-field__control),
:deep(.q-field .q-field__native) {
  min-height: 32px;
  height: 42px;
}
:deep(.q-field .q-checkbox__label) {
  color: rgba(0, 0, 0, 0.75);
  font-size: 12px;
  line-height: 1.25;
  font-weight: 400;
  letter-spacing: 0.00937em;
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
:deep(.q-field.q-field--readonly .q-field__control:before) {
  border-bottom-style: dashed;
}
:deep(.q-field .q-field__control:before) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  transition: border-color 0.36s cubic-bezier(0.4, 0, 0.2, 1);
}
:deep(.q-field__messages > div) {
  line-height: 1.3;
}
</style>
