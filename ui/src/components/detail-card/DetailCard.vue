<template>
  <q-card flat bordered class="detail-card">
    <q-item dense class="q-pb-none q-px-sm bg-grey-2 text-grey-7">
      <q-item-section v-if="icon" side class="q-pr-sm">
        <q-icon :name="icon" color="grey-6" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label class="text-subtitle2">
          {{ title }}
          <q-badge v-if="badgeValue" rounded color="purple-4" align="middle" label="badgeValue" />
        </q-item-label>
      </q-item-section>
      <template v-if="showFilter">
        <q-input
          dense
          standout="bg-indigo-6"
          hide-bottom-space
          v-model="cardFilter"
          debounce="300"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="Filter"
          class="card-title-search"
          color="indigo-9"
        >
          <template v-slot:append>
            <q-icon v-if="cardFilter === ''" name="search" color="blue-grey-5" size="14px" />
            <q-icon
              v-else
              name="highlight_off"
              class="cursor-pointer"
              color="blue-grey-5"
              size="14px"
              @click="cardFilter = ''"
            />
          </template>
        </q-input>
      </template>
      <EditButtons
        v-if="editable"
        :linkable="data.link"
        cancellable
        :main-icon="editIcon"
        :main-color="editColour"
        :show-main="!saving"
        :show-cancel="markdown && editOn && editor.hasChanged"
        :show-spinner="saving"
        @navigate="router.push(linkTarget)"
        @action="editOn = !editOn"
        @cancel="editor?.onCancel"
      />
    </q-item>
    <q-separator class="bg-grey-4" />
    <q-card-section :class="padContainer ? 'q-pa-md' : 'q-pa-none'">
      <template v-if="fields && data">
        <template v-for="field in fields" :key="field">
          <ValueDisplay
            :ref="(el) => register(field, el)"
            :data="data[field]"
            :field="field"
            @value-changed="valueChanged"
          />
        </template>
      </template>
      <template v-else-if="markdown">
        <MarkdownEditor
          ref="md-editor"
          :text="data.value"
          in-card
          @onSaveText="valueChanged"
          :placeholder="data.placeholder"
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
import ValueDisplay from "./ValueDisplay.vue";
import { MarkdownEditor } from "@/components";
import { isObject } from "@/utils";
import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "DetailCard",
  components: {
    EditButtons,
    MarkdownEditor,
    ValueDisplay,
  },
  emits: ["valueChanged"],
  props: {
    icon: String,
    title: {
      type: String,
      required: true,
    },
    noData: {
      type: String,
      default: "There is no data to show.",
    },
    badgeValue: Number,
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
    fields: Array,
    data: Object,
    register: Function,
    fieldName: String,
    markdown: {
      type: Boolean,
      default: false,
    },
  },

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

<style lang="scss">
.detail-card {
  border-color: rgb(209, 209, 209);
}
.card-title-search {
  width: 30%;
}
.card-title-search .q-field__control {
  font-size: 12px;
  height: 23px;
  border: 1px solid rgb(209, 209, 209);
  border-radius: 4px;
  padding: 0px 5px 0px 10px;
}
.card-title-search .q-field__native,
.card-title-search .q-field__marginal {
  height: 21px;
  padding: 6px 10px;
  color: #777;
}
.card-title-search .q-field__inner {
  align-self: center;
}
.q-field--standard.q-field--readonly .q-field__control:before,
.q-field--readonly .q-field__control:before {
  border-bottom: 1px dotted rgba(0, 0, 0, 0.24);
}
.value-display .q-field__append {
  height: auto;
}
.value-display .q-field--labeled .q-field__native {
  padding-bottom: 0;
}
.value-display .q-chip {
  font-size: 12px;
  padding: 0.5em 0.9em;
  height: 1.7em;
  background: transparent;
  border: 1px solid #303f9f;
}
.value-display .q-chip--dense .q-chip__icon--remove {
  margin-left: 0.3em;
  margin-right: -0.5em;
}
</style>
