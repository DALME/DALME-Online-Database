<template>
  <div class="column q-my-sm">
    <q-btn
      round
      color="amber"
      text-color="black"
      size="xs"
      icon="add"
      class="q-mr-auto q-mt-sm"
      @click.stop="handleAdd"
    >
      <q-tooltip
        class="bg-blue z-max"
        transition-show="scale"
        transition-hide="scale"
        anchor="center right"
        self="center right"
        :offset="[100, 0]"
      >
        Add an attribute
      </q-tooltip>
    </q-btn>
    <template v-for="(item, idx) in fieldData" :key="idx">
      <div class="row items-center">
        <div class="col-5 q-pr-sm">
          <q-select
            use-input
            hide-bottom-space
            input-debounce="350"
            label="Attribute"
            :model-value="item.attribute.name"
            :options="options"
            :option-value="(option) => option.id"
            :option-label="(option) => option.name"
            :popup-content-style="{ zIndex: '9999 !important' }"
            @update:modelValue="onUpdate(value, idx)"
          />
        </div>
        <div class="col-7 q-pl-sm">
          <q-input
            clearable
            hide-bottom-space
            debounce="500"
            label="Value"
            :model-value="item.value"
            @update:modelValue="onUpdate(value, idx)"
          >
            <template v-slot:after v-if="fieldData.length > 1">
              <q-btn
                round
                color="amber"
                text-color="black"
                size="xs"
                icon="delete"
                @click.stop="handleRemove(idx)"
              />
            </template>
          </q-input>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  name: "AttributesField",
  props: {
    modelValue: {
      type: Array,
    },
    validation: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, context) {
    // const options = ref(null);
    const options = [
      { id: 1, name: "Web address" },
      { id: 2, name: "Mk.II ID" },
    ];

    const empty = { attribute: { id: null, name: null }, value: null };
    const data = ref([empty]);
    const fieldData = computed(() => props.modelValue || data.value);

    const error = computed(() => props.validation.errors.length > 0);
    const onUpdate = (value, idx) => {
      console.assert(idx);
      context.emit("update:modelValue", value);
    };

    const handleAdd = () => data.value.push(empty);
    const handleRemove = (idx) => data.value.splice(idx, 1);

    return {
      fieldData,
      handleAdd,
      handleRemove,
      error,
      onUpdate,
      options,
    };
  },
});
</script>
