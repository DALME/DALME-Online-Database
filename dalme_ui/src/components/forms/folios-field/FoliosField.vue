<template>
  <div class="folios-field column q-my-sm" :class="{ separator: !showing }">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{
          !showing && modelValue !== [empty()]
            ? `Folios (${modelValue.length})`
            : "Folios"
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
            <div
              class="justify-center q-py-md q-pr-md text-grey text-subtitle2"
            >
              #{{ idx + 1 }}
            </div>
            <div class="col-5 q-pr-sm">
              <InputField
                label="Folio"
                v-model="data.folio"
                :field="`folios[${idx}].folio`"
                :validation="validators.folio"
              />
            </div>
            <div class="q-pl-sm col-4">
              <SelectField
                label="DAM ID"
                v-model="data.damId"
                :field="`folios[${idx}].damId`"
                :filterable="true"
                :getOptions="getImageOptions"
                :optionsSchema="imageOptionsSchema"
                :validation="validators.damId"
              />
            </div>
            <div class="q-pl-sm col">
              <div class="row flex-center full-height">
                <q-btn
                  flat
                  round
                  push
                  icon="search"
                  :color="!data.damId ? 'grey' : 'black'"
                  :disable="!data.damId"
                  @click.stop="card = true"
                >
                  <q-dialog class="z-max" v-model="card" :key="idx">
                    <q-img :src="getPreview(data.damId.value)">
                      <template v-slot:error>
                        <div
                          class="absolute-full flex flex-center bg-negative text-white"
                        >
                          Couldn't load preview
                        </div>
                      </template>
                    </q-img>
                  </q-dialog>

                  <q-tooltip class="bg-blue z-max"> Preview folio </q-tooltip>
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
                icon="swap_vert"
                :disable="modelValue.length < 2"
                :color="modelValue.length < 2 ? 'grey' : 'black'"
                @click.stop.prevent="handleDrag(idx)"
              />
              <q-btn
                class="q-ml-auto"
                flat
                round
                unelevated
                size="xs"
                icon="clear"
                @click.stop="handleRemoveField(idx)"
              />
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
import { filter as rFilter, isNil, reduce, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineComponent, ref, unref } from "vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import { imageOptionsSchema } from "@/schemas";

export default defineComponent({
  name: "FoliosField",
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    validators: {
      required: true,
    },
  },
  components: {
    InputField,
    SelectField,
  },
  setup(props, context) {
    const empty = () => ({ folio: null, damId: null });

    const { fields, push, replace } = useFieldArray("folios");

    const card = ref(false);
    const loading = ref(false);
    const showing = ref(props.modelValue.length > 0 ? true : false);

    const handleAddField = () => {
      const newValue = unref(props.modelValue);
      context.emit("update:modelValue", [...newValue, empty()]);
      push(empty());
    };
    const handleRemoveField = (idx) => {
      const newValue = unref(props.modelValue);
      newValue.splice(idx, 1);
      context.emit("update:modelValue", newValue);
      replace(newValue);
    };
    const handleDrag = (idx) => {
      console.assert(idx);
    };

    const indexed = computed(() => {
      const reducer = (acc, row) => {
        if (!isNil(row.damId)) {
          acc.add(row.damId.value);
        }
        return acc;
      };
      return reduce(reducer, new Set(), props.modelValue);
    });

    const filterImageOptions = (options) =>
      // TODO: dam_id -> damId when camelCase renderer is added.
      rFilter((option) => !indexed.value.has(option.dam_id), options);

    const getImageOptions = () =>
      fetcher(requests.images.getImageOptions())
        .then((response) => response.json())
        .then((options) => filterImageOptions(options));

    const getPreview = (damId) => {
      const url = ref(null);
      fetcher(requests.images.getImageUrl(damId))
        .then((response) => response.json())
        .then((data) => (url.value = data.url));
      return url;
    };

    return {
      card,
      empty,
      fields,
      filterImageOptions,
      getImageOptions,
      getPreview,
      handleAddField,
      handleDrag,
      handleRemoveField,
      imageOptionsSchema,
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
</style>
