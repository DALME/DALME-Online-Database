<template>
  <div v-if="!loading" class="date-field">
    <div :class="editOn ? 'field-date-container active' : 'field-date-container'">
      <div class="field-date-wrapper">
        <div class="field-date-label q-field__label">
          <div>{{ fieldLabel }}</div>
        </div>
        <DateChooser @changed="onValueChanged" :data="value" :editable="editOn" />
      </div>
      <div class="field-date-buttons">
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
      </div>
    </div>
    <template v-if="fieldDescription">
      <div class="field-description">{{ fieldDescription }}</div>
    </template>
  </div>
</template>

<script>
import { defineComponent, onBeforeMount } from "vue";
import { useRouter } from "vue-router";

import { DateChooser } from "@/components";
import { useEditing } from "@/use";
import { nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "DateField",
  components: { EditButtons, DateChooser },
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
      required: true,
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
      required: true,
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
      onValueChanged,
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
      loading,
      nully,
      onAction,
      onCancel,
      router,
      saving,
      onValueChanged,
      value,
      onRemove,
    };
  },
});
</script>

<style lang="scss" scoped>
.date-field {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: baseline;
  flex-direction: column;
}
.date-field label {
  width: 100%;
}
.field-date-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-bottom: 1px dotted rgba(0, 0, 0, 0.24);
  height: 57px;
}
.field-date-container::after {
  content: "";
  pointer-events: none;
  height: 2px;
  border-bottom-left-radius: inherit;
  border-bottom-right-radius: inherit;
  transform-origin: center bottom;
  transform: scale3d(0, 1, 1);
  background: rgb(48, 63, 159);
  transition: transform 0.36s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-self: end;
  position: absolute;
  left: 16px;
  right: 16px;
  margin-bottom: -1px;
}
.field-date-container.active::after {
  transform: scale3d(1, 1, 1);
}
.field-date-wrapper {
  display: flex;
  flex-direction: column;
}
.field-date-buttons {
  display: flex;
  margin-left: auto;
  height: auto;
  align-items: center;
  margin-top: 22px;
}
.field-date-label {
  transform: scale(0.75);
  height: 24px;
}
.field-date-label div:first-child {
  position: absolute;
  bottom: -10px;
}
.date-chooser-wrapper {
  height: 32px;
}
.field-description {
  font-size: 11px;
  color: rgb(107 117 175 / 77%);
  min-height: 20px;
  line-height: 1;
  padding: 4px 0 0;
  backface-visibility: hidden;
  line-height: 1.3;
}
</style>
