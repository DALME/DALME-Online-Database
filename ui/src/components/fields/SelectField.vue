<template>
  <div v-if="!loading" :class="classes">
    <q-select
      :ref="`input${uniqueKey}`"
      v-model="value"
      @filter="onFilterOptions"
      :class="showBottom ? '' : 'no-hint'"
      :hint="fieldDescription"
      :label="fieldLabel"
      :multiple="multiple"
      :options="filteredOptions"
      :readonly="!editOn"
      :rules="[validate]"
      :use-chips="multiple"
      color="indigo-8"
      input-debounce="0"
      popup-content-class="value-select-popup"
      emit-value
      hide-bottom-space
      hide-dropdown-icon
      map-options
      menu-shrink
      options-dense
      stack-label
      use-input
    >
      <template v-if="repository.entity === 'user'" #option="scope">
        <q-item v-bind="scope.itemProps" dense>
          <q-item-section side>
            <q-avatar v-if="!nully(scope.opt.icon)" size="34px">
              <q-img :src="scope.opt.icon" class="chooser-avatar-image" fit="cover" ratio="1" />
            </q-avatar>
            <q-icon v-else color="grey-4" name="mdi-account-circle" size="34px" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ scope.opt.label }}</q-item-label>
            <q-item-label caption>{{ scope.opt.detail }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>
      <template v-if="multiple" #selected-item="scope">
        <q-chip
          @remove="scope.removeAtIndex(scope.index)"
          :icon="chipIcon"
          :label="scope.opt.label"
          :removable="editOn"
          color="deep-purple-6"
          size="sm"
          text-color="white"
          clickable
          outline
        />
      </template>
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
    </q-select>
  </div>
</template>

<script>
import { computed, defineComponent, onBeforeMount, useTemplateRef } from "vue";
import { useRouter } from "vue-router";

import { useEditing } from "@/use";
import { isObject, nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "SelectField",
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
      default: "Select",
    },
    editable: {
      type: Boolean,
      required: false,
      default: true,
    },
    sidebar: {
      type: Boolean,
      required: false,
      default: false,
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
    multiple: {
      type: Boolean,
      required: false,
      default: false,
    },
    chipIcon: {
      type: String,
      required: false,
      default: "mdi-circle-medium",
    },
  },
  emits: ["drop", "created", "destroyed"],

  setup(props, context) {
    const uniqueKey = crypto.randomUUID();
    const input = useTemplateRef(`input${uniqueKey}`);
    const router = useRouter();

    const cleanValue = (value) => {
      console.log("cleanValue", value);
      if (Array.isArray(value)) return value.map((v) => (isObject(v) ? v.id : v));
      if (isObject(value)) return value.id;
      return value;
    };

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
      onFilterOptions,
      options,
      filteredOptions,
      optionsField,
    } = useEditing(props, context, input, cleanValue);

    const classes = computed(() => {
      const cls = ["select-field"];
      if (props.sidebar) cls.push("sidebar");
      if (editOn.value) cls.push("editing");
      return cls.length ? cls.join(" ") : "";
    });

    onBeforeMount(() => {
      loading.value = true;
      record.value = props.repository.find(props.id);
      props.repository.options(optionsField.value).then((result) => {
        options.value = result;
        filteredOptions.value = options.value;
        value.value = cleanValue(record.value[dataField.value]);
        loading.value = false;
        console.log(
          `SELECT mounted ${fieldLabel.value}`,
          value.value,
          record.value,
          dataField.value,
          options.value,
        );
      });
    });

    return {
      classes,
      editOn,
      fieldDescription,
      fieldLabel,
      filteredOptions,
      hasChanged,
      isAttribute,
      isObject,
      loading,
      nully,
      onAction,
      onCancel,
      onFilterOptions,
      onRemove,
      router,
      saving,
      showBottom,
      uniqueKey,
      validate,
      value,
    };
  },
});
</script>

<style lang="scss" scoped>
.select-field {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: baseline;
}
.select-field label {
  width: 100%;
}
:deep(.q-field .q-field__control .q-field__append) {
  margin-top: 22px;
}
:deep(.q-field__native) {
  padding: 0;
}
:deep(.q-select--with-input.q-field--readonly .q-field__native input) {
  display: none;
}
:deep(.q-field__marginal) {
  height: auto;
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
// sidebar version
// additional global overrides in src/css/field-overrides.scss
.select-field.sidebar {
  margin-bottom: 12px;
}
</style>
