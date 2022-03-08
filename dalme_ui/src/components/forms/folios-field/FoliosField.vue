<template>
  <div class="folios-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && modelValue !== [empty()]
            ? `folios (${modelValue.length})`
            : "folios"
        }}
      </div>

      <q-spinner v-if="loading" color="primary" size="xs" />
      <q-btn
        v-show="showing"
        round
        class="q-ml-sm"
        color="amber"
        icon="add"
        size="xs"
        text-color="black"
        @click.stop="handleAddField"
      >
        <q-tooltip class="bg-blue z-max"> Add a folio </q-tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <q-tooltip class="bg-blue z-max">
          {{ showing ? "Hide folios" : "Show folios" }}
        </q-tooltip>
      </q-btn>
    </div>

    <template v-if="showing">
      <template v-if="modelValue.length > 0">
        <template
          v-for="({ 0: data, 1: field }, idx) in zip(modelValue, fields)"
          :key="field.key"
        >
          <div class="row q-mb-sm" v-show="showing">
            <div class="col-6 q-pr-sm">
              <SelectField
                field="folio"
                label="Folio"
                :model-value="data.folio"
                :filterable="true"
                :getOptions="getFolioOptions(idx)"
                :optionsSchema="folioOptionsSchema"
                :validation="validators.folio"
                @clear="() => handleClearFolio(idx)"
                @update:modelValue="(value) => handleUpdateFolio(value, idx)"
              />
            </div>
            <div class="q-pl-sm col-4">
              <SelectField
                field="damId"
                :disable="!data.folio"
                :label="data.folio ? 'DAM ID' : 'Choose a folio'"
                :model-value="data.damId"
                :filterable="true"
                :getOptions="getDamIdOptions(idx)"
                :optionsSchema="damIdOptionsSchema"
                :validation="validators.damId"
                @update:modelValue="(value) => handleUpdateDamId(value, idx)"
              />
            </div>
            <div class="q-pl-sm col">
              <div class="row flex-center full-height">
                <q-btn
                  flat
                  round
                  icon="search"
                  :color="!(data.folio && data.damId) ? 'grey' : 'black'"
                  :disable="!(data.folio && data.damId)"
                >
                  <q-tooltip class="bg-blue z-max"> Add note </q-tooltip>
                </q-btn>
              </div>
            </div>

            <div class="row items-center">
              <q-btn
                class="q-ml-auto"
                flat
                round
                unelevated
                size="xs"
                icon="clear"
                @click.stop="handleRemoveField(idx)"
              >
              </q-btn>
            </div>
          </div>
        </template>
      </template>
      <template v-else>
        <div class="text-subtitle1 placeholder">
          <p>No folios referenced.</p>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import { isNil, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import { defineComponent, inject, ref } from "vue";

import { fetcher } from "@/api";
import { SelectField } from "@/components/forms";

export default defineComponent({
  name: "FoliosField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    validators: {
      type: Object,
      required: true,
    },
  },
  components: {
    SelectField,
  },
  setup(props, context) {
    const empty = () => ({ folio: null, damId: null });

    const { fields, push, remove } = useFieldArray("folios");

    const cuid = inject("cuid");

    const loading = ref(false);
    const showing = ref(true);

    const handleAddField = () => {
      push(empty());
      const newValue = props.modelValue.slice(0);
      context.emit("update:modelValue", [...newValue, empty()]);
      context.emit("change");
    };
    const handleRemoveField = (idx) => {
      remove(idx);
      const newValue = props.modelValue.slice(0);
      newValue.splice(idx, 1);
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };
    const handleClearFolio = (idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx] = empty();
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };
    const handleUpdateFolio = (value, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx].agent = !isNil(value) ? value : null;
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };
    const handleUpdateRole = (value, idx) => {
      const newValue = props.modelValue.slice(0);
      newValue[idx].role = !isNil(value) ? value : null;
      context.emit("update:modelValue", newValue);
      context.emit("change");
    };

    // const references = computed(() => {});

    const filterFolioOptions = (idx, options) => options;
    const filterDamIdOptions = (idx, options) => options;

    const getFolioOptions = (idx) =>
      fetcher(null)
        .then((response) => response.json())
        .then((options) => filterFolioOptions(idx, options));
    const getDamIdOptions = (idx) =>
      fetcher(null)
        .then((response) => response.json())
        .then((options) => filterDamIdOptions(idx, options));

    return {
      cuid,
      empty,
      fields,
      filterFolioOptions,
      filterDamIdOptions,
      getFolioOptions,
      getDamIdOptions,
      handleAddField,
      handleClearFolio,
      handleUpdateFolio,
      handleUpdateRole,
      handleRemoveField,
      loading,
      showing,
      zip,
    };
  },
});
</script>

<style lang="scss" scoped>
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
.folios-field .q-field__after,
.folios-field .q-field__append {
  padding-left: 0 !important;
}
.folios-field .q-field--with-bottom {
  padding-bottom: 0;
}
.folio-select .q-field__native {
  color: black;
}
.placeholder {
  align-items: center;
  border-bottom: 1px solid #c2c2c2;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 400;
  letter-spacing: 0.00937em;
  line-height: 18px;
  margin-bottom: 8px;
  padding-bottom: 17px;
  padding-top: 20px;
}
.placeholder > p {
  margin: 0;
}
// div.q-dialog__title {
//   font-size: 1rem;
// }
</style>
