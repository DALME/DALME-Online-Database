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
        <Tooltip> Add a folio </Tooltip>
      </q-btn>

      <q-btn
        round
        class="q-ml-sm"
        size="xs"
        :icon="showing ? 'visibility_off' : 'visibility'"
        @click.stop="showing = !showing"
      >
        <Tooltip>
          {{ showing ? "Hide folios" : "Show folios" }}
        </Tooltip>
      </q-btn>

      <Tooltip v-if="description">
        {{ description }}
      </Tooltip>
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
                  :color="!data.damId || !data.hasImage ? 'grey' : 'black'"
                  :disable="!data.damId || !data.hasImage"
                  @click.stop="() => handlePreview(data.damId)"
                >
                  <Tooltip> Preview folio </Tooltip>
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
                :disable="true"
                color="grey"
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
import cuid from "cuid";
import { filter as rFilter, isNil, reduce, zip } from "ramda";
import { useFieldArray } from "vee-validate";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  onMounted,
  ref,
  unref,
} from "vue";
import { useActor } from "@xstate/vue";

import { fetcher, requests } from "@/api";
import { InputField, SelectField } from "@/components/forms";
import { imageOptionsSchema } from "@/schemas";
import { useEditing } from "@/use";

import { empty } from "./normalize";

export default defineComponent({
  name: "FoliosField",
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
      required: true,
    },
  },
  components: {
    InputField,
    SelectField,
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup(props, context) {
    const {
      editingIndex,
      modals,
      machine: { send },
    } = useEditing();
    const { fields, replace } = useFieldArray("folios");

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
        send("SET_FOCUS", { value: indexed.cuid });
        actorSend("SHOW");
      } else {
        send("SPAWN_FOLIO", {
          cuid: cuid(),
          key,
          metadata: { damId },
        });
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
.folios-field {
  will-transform: auto;
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
.separator {
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  padding-bottom: 0.5rem;
}
</style>
