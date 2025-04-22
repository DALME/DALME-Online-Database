<template>
  <q-card class="detail-card" bordered flat>
    <q-item class="q-pb-none q-px-sm bg-grey-2 text-grey-7" dense>
      <q-item-section v-if="icon" class="q-pr-sm" side>
        <q-icon :name="icon" color="grey-6" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label class="text-subtitle2">
          {{ title }}
          <q-badge v-if="badgeValue" align="middle" color="purple-4" label="badgeValue" rounded />
        </q-item-label>
      </q-item-section>
      <template v-if="showFilter">
        <q-input
          v-model="cardFilter"
          autocapitalize="off"
          autocomplete="off"
          autocorrect="off"
          class="card-title-search"
          color="indigo-9"
          debounce="300"
          placeholder="Filter"
          spellcheck="false"
          standout="bg-indigo-6"
          dense
          hide-bottom-space
        >
          <template #append>
            <q-icon v-if="cardFilter === ''" color="blue-grey-5" name="search" size="14px" />
            <q-icon
              v-else
              @click="cardFilter = ''"
              class="cursor-pointer"
              color="blue-grey-5"
              name="highlight_off"
              size="14px"
            />
          </template>
        </q-input>
      </template>
      <EditButtons
        v-if="editable"
        @action="editOn = !editOn"
        @cancel="editor?.onCancel"
        @navigate="router.push(linkTarget)"
        :linkable="data.link"
        :main-color="editColour"
        :main-icon="editIcon"
        :show-cancel="markdown && editOn && editor.hasChanged"
        :show-main="!saving"
        :show-spinner="saving"
        cancellable
      />
    </q-item>
    <q-separator class="bg-grey-4" />
    <q-card-section :class="padContainer ? 'q-pa-md' : 'q-pa-none'">
      <template v-if="fields && data">
        <template v-for="field in fields" :key="field">
          <ValueDisplay
            :ref="(el) => register(field, el)"
            @value-changed="valueChanged"
            :data="data[field]"
            :field="field"
          />
        </template>
      </template>
      <template v-else-if="markdown">
        <MarkdownEditor
          ref="md-editor"
          @on-save-text="valueChanged"
          :placeholder="data.placeholder"
          :text="data.value"
          in-card
        />
      </template>
      <slot v-else>
        {{ noData }}
      </slot>
    </q-card-section>
  </q-card>
</template>

<script>
import { computed, defineComponent, provide, ref, useTemplateRef } from "vue";

import { MarkdownEditor } from "@/components";
import { isObject } from "@/utils";

import EditButtons from "./EditButtons.vue";
import ValueDisplay from "./ValueDisplay.vue";

export default defineComponent({
  name: "DetailCard",
  components: {
    EditButtons,
    MarkdownEditor,
    ValueDisplay,
  },
  props: {
    icon: {
      type: String,
      required: false,
      default: "mdiInformationBox",
    },
    title: {
      type: String,
      required: true,
    },
    noData: {
      type: String,
      default: "There is no data to show.",
    },
    badgeValue: {
      type: Number,
      required: false,
      default: null,
    },
    showFilter: {
      type: Boolean,
      default: false,
    },
    padContainer: {
      type: Boolean,
      default: false,
    },
    editable: {
      type: Boolean,
      default: false,
    },
    fields: {
      type: Array,
      required: false,
      default: null,
    },
    data: {
      type: Object,
      required: false,
      default: null,
    },
    register: {
      type: Function,
      required: true,
    },
    fieldName: {
      type: String,
      required: true,
    },
    markdown: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["valueChanged"],

  setup(props, context) {
    const cardFilter = ref("");
    const editor = useTemplateRef("md-editor");
    const editOn = ref(false);
    const saving = ref(false);
    const isNew = ref(props.data?.value === null && props.data?.show === true);

    const editIcon = computed(() =>
      editOn.value
        ? editor.value.hasChanged
          ? "mdi-content-save-outline"
          : "mdi-close-circle-outline"
        : "mdi-cog-outline",
    );

    const editColour = computed(() =>
      editOn.value ? (editor.value.hasChanged ? "green-6" : "orange-6") : "grey-5",
    );

    const valueChanged = (value) => {
      const baseAttr = {
        name: props.fieldName,
        update: !isNew.value,
        source: props.data.source,
        id: props.data.id,
      };
      if (isObject(value) && "name" in value) {
        context.emit("valueChanged", value);
      } else {
        const valObj = isObject(value) ? value : { value: value, oldValue: props.data.value };
        context.emit("valueChanged", Object.assign(valObj, baseAttr));
      }
    };

    provide("cardFilter", cardFilter);
    provide("editOn", editOn);

    return {
      cardFilter,
      editOn,
      editIcon,
      editColour,
      editor,
      saving,
      valueChanged,
    };
  },
});
</script>

<style lang="scss" scoped>
.detail-card {
  border-color: rgb(209, 209, 209);
}
.card-title-search {
  width: 30%;
}
:deep(.card-title-search .q-field__control) {
  font-size: 12px;
  height: 23px;
  border: 1px solid rgb(209, 209, 209);
  border-radius: 4px;
  padding: 0px 5px 0px 10px;
}
:deep(.q-item__label) {
  font-size: 13px;
}
:deep(.card-title-search .q-field__native),
:deep(.card-title-search .q-field__marginal) {
  height: 21px;
  padding: 6px 10px;
  color: #777;
}
:deep(.card-title-search .q-field__inner) {
  align-self: center;
}
:deep(.q-field--standard.q-field--readonly .q-field__control:before),
:deep(.q-field--readonly .q-field__control:before) {
  border-bottom: 1px dotted rgba(0, 0, 0, 0.24);
}
:deep(.value-display .q-field__append) {
  height: auto;
}
:deep(.value-display .q-field--labeled .q-field__native) {
  padding-bottom: 0;
}
:deep(.value-display .q-chip) {
  font-size: 12px;
  padding: 0.5em 0.9em;
  height: 1.7em;
  background: transparent;
  border: 1px solid #303f9f;
}
:deep(.value-display .q-chip--dense .q-chip__icon--remove) {
  margin-left: 0.3em;
  margin-right: -0.5em;
}
</style>
