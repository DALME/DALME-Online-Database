<template>
  <div :class="{ separator: !showing }" class="folios-field column q-my-sm">
    <div class="row items-center q-my-sm">
      <div class="q-field__label no-pointer-events q-mr-auto">
        {{ !showing && !empty(modelValue) ? `Folios (${modelValue.length})` : "Folios" }}
      </div>

      <q-spinner v-if="loading" color="primary" size="xs" />
      <q-btn
        v-show="showing"
        @click.stop="handleAddField"
        class="q-ml-sm"
        color="amber"
        icon="add"
        size="xs"
        text-color="black"
        round
      >
        <ToolTip> Add a folio </ToolTip>
      </q-btn>

      <q-btn
        @click.stop="showing = !showing"
        :icon="showing ? 'visibility_off' : 'visibility'"
        class="q-ml-sm"
        size="xs"
        round
      >
        <ToolTip>
          {{ showing ? "Hide folios" : "Show folios" }}
        </ToolTip>
      </q-btn>

      <ToolTip v-if="description">
        {{ description }}
      </ToolTip>
    </div>

    <template v-if="showing">
      <template v-if="modelValue.length > 0">
        <template v-for="({ 0: data, 1: field }, idx) in zip(modelValue, fields)" :key="field.key">
          <div v-show="showing" class="row q-mb-sm">
            <div class="justify-center q-py-md q-pr-md text-grey text-subtitle2">
              #{{ idx + 1 }}
            </div>
            <div class="col-5 q-pr-sm">
              <InputField
                v-model="data.folio"
                :field="`folios[${idx}].folio`"
                :validation="validators.folio"
                label="Folio"
              />
            </div>
            <div class="q-pl-sm col-4">
              <SelectField
                v-model="data.damId"
                :field="`folios[${idx}].damId`"
                :filterable="true"
                :get-options="getImageOptions"
                :options-schema="imageOptionsSchema"
                :validation="validators.damId"
                label="DAM ID"
              />
            </div>
            <div class="q-pl-sm col">
              <div class="row flex-center full-height">
                <q-btn
                  @click.stop="() => handlePreview(data.damId)"
                  :color="!data.damId || !data.hasImage ? 'grey' : 'black'"
                  :disable="!data.damId || !data.hasImage"
                  icon="search"
                  flat
                  push
                  round
                >
                  <ToolTip> Preview folio </ToolTip>
                </q-btn>
              </div>
            </div>

            <div class="row items-center">
              <q-btn
                @click.stop.prevent="handleDrag(idx)"
                :disable="true"
                class="q-ml-auto"
                color="grey"
                icon="swap_vert"
                size="xs"
                flat
                round
                unelevated
              />
              <q-btn
                @click.stop="confirm = true"
                class="q-ml-auto"
                icon="clear"
                size="xs"
                flat
                round
                unelevated
              >
                <q-dialog v-model="confirm" class="z-max" persistent>
                  <q-card>
                    <q-card-section class="row items-center">
                      <q-avatar color="red" icon="warning" size="sm" text-color="white" />
                      <span class="q-ml-sm"> Are you sure you want to remove this folio? </span>
                    </q-card-section>

                    <q-card-actions align="right">
                      <q-btn v-close-popup color="primary" label="Cancel" flat />
                      <q-btn
                        v-close-popup
                        @click.stop="handleRemoveField(idx)"
                        color="red"
                        label="Remove"
                        flat
                      />
                    </q-card-actions>
                  </q-card>
                </q-dialog>
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
import { createId as cuid } from "@paralleldrive/cuid2";
import { useActor } from "@xstate/vue";
import { isNil, filter as rFilter, reduce, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import { computed, defineAsyncComponent, defineComponent, onMounted, ref, unref } from "vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import { imageOptionsSchema } from "@/schemas";
import { useEditing } from "@/use";

import { empty } from "./normalize";

export default defineComponent({
  name: "FoliosField",
  components: {
    InputField,
    SelectField,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    description: {
      type: [Boolean, String],
      default: () => false,
    },
    validators: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:modelValue"],

  setup(props, context) {
    const {
      editingIndex,
      modals,
      machine: { send },
    } = useEditing();
    const { fields, replace } = useFieldArray("folios");

    const confirm = ref(false);
    const loading = ref(false);
    const showing = ref(!props.modelValue.length > 0);

    const handleAddField = () => {
      const newValue = [...unref(props.modelValue), empty()];
      replace(newValue);
      context.emit("update:modelValue", newValue);
    };
    const handleRemoveField = (idx) => {
      const newValue = unref(props.modelValue);
      newValue.splice(idx, 1);
      replace(newValue);
      context.emit("update:modelValue", newValue);
      confirm.value = false;
    };
    const handleDrag = (idx) => {
      // TODO: Implement dragging re-order.
      console.assert(idx);
    };
    const handlePreview = ({ value: damId }) => {
      const key = `folio-${damId}`;
      const indexed = editingIndex.value[key];
      if (!isNil(indexed)) {
        const { send: actorSend } = useActor(modals.value[indexed.cuid].actor);
        send({ type: "SET_FOCUS", value: indexed.cuid });
        actorSend({ type: "SHOW" });
      } else {
        send({ type: "SPAWN_FOLIO", cuid: cuid(), key, metadata: { damId } });
      }
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

    // TODO: Use fetchAPI and a schema here please.
    const getImageOptions = () =>
      fetcher(requests.images.getImageOptions())
        .then((response) => response.json())
        .then((options) => filterImageOptions(options));

    // NOTE: Not sure why we need to do this here but not on AgentsField, but
    // it doesn't render correctly otherwise.
    onMounted(async () => {
      if (props.modelValue.length > 0) {
        const newValue = unref(props.modelValue);
        replace(newValue);
      }
    });

    return {
      confirm,
      empty,
      fields,
      filterImageOptions,
      getImageOptions,
      handleAddField,
      handleDrag,
      handlePreview,
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
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
</style>
