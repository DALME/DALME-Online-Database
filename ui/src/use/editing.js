import { computed, ref } from "vue";

import { validators } from "@/schemas";

export const useEditing = (props, context, input = null, modValue = null) => {
  // state
  const editOn = ref(false);
  const filteredOptions = ref([]);
  const loading = ref(false);
  const options = ref([]);
  const record = ref(null);
  const saving = ref(false);
  const value = ref(null);

  // getters
  const repository = computed(() => props.repository);
  const isAttribute = computed(() => repository.value.entity === "attribute");
  const dataField = computed(() => (isAttribute.value ? "value" : props.field));
  const optionsField = computed(() => (isAttribute.value ? record.value.name : props.field));
  const fieldLabel = computed(() => (isAttribute.value ? record.value.label : props.label));
  const fieldDescription = computed(() =>
    isAttribute.value ? record.value.description : props.description,
  );
  const hasChanged = computed(() => processValue(record.value[dataField.value]) !== value.value);
  const validator = computed(() => validators[dataField.value]);
  const showBottom = computed(() => fieldDescription.value || input?.value?.hasError);

  // actions
  const onAction = () => {
    if (editOn.value && hasChanged.value) {
      saving.value = true;
      if (props.creating) {
        repository.value
          .create({ ...props.defaults, [dataField.value]: value.value })
          .then((newRecord) => {
            saving.value = false;
            editOn.value = !editOn.value;
            context.emit("created", newRecord);
          });
      } else {
        repository.value.update(props.id, { [dataField.value]: value.value }).then(() => {
          saving.value = false;
          editOn.value = !editOn.value;
        });
      }
    } else {
      editOn.value = !editOn.value;
    }
  };

  const onCancel = () => {
    if (props.creating) {
      context.emit("drop");
    } else {
      value.value = processValue(record.value[dataField.value]);
    }
  };

  const onRemove = () => {
    repository.value.destroy(props.id).then(() => {
      context.emit("destroyed", props.id);
    });
  };

  const onFilterOptions = (query, update) => {
    if (query === "") {
      update(() => (filteredOptions.value = options.value));
      return;
    }
    update(() => {
      filteredOptions.value = options.value.filter(
        (x) => x.label.toLowerCase().indexOf(query.toLowerCase()) > -1,
      );
    });
  };

  const onValueChanged = (value) => {
    value.value = value;
  };

  const processValue = (value) => {
    if (modValue) return modValue(value);
    return value;
  };

  const validate = (value) => {
    if (!validator.value) return Promise.resolve(true);
    return validator.value
      .validate(value)
      .then(() => true)
      .catch((error) => error.errors[0]);
  };

  return {
    dataField,
    editOn,
    fieldDescription,
    fieldLabel,
    filteredOptions,
    hasChanged,
    isAttribute,
    loading,
    onAction,
    onCancel,
    onFilterOptions,
    onRemove,
    onValueChanged,
    options,
    optionsField,
    record,
    saving,
    showBottom,
    validate,
    value,
  };
};
