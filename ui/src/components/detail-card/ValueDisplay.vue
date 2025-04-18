<template>
  <div v-if="!loading" class="value-display">
    <q-input
      v-if="data.dataType === 'STR'"
      v-model="value"
      :label="data.label"
      :placeholder="data.description ? data.description : null"
      :readonly="!editOn"
      color="indigo-8"
      autogrow
    >
      <template #append>
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          @navigate="router.push(linkTarget)"
          :linkable="data.link"
          :main-color="editColour"
          :main-icon="editIcon"
          :show-cancel="editOn && hasChanged"
          :show-link="!saving && !editOn"
          :show-main="data.editable && !saving"
          :show-spinner="saving"
          cancellable
        />
      </template>
    </q-input>
    <q-select
      v-if="data.dataType === 'FKEY'"
      v-model="value"
      @filter="optionsFilter"
      :label="data.label"
      :multiple="multiple"
      :options="options"
      :readonly="!editOn"
      :use-chips="multiple"
      color="indigo-8"
      input-debounce="0"
      emit-value
      hide-dropdown-icon
      map-options
      menu-shrink
      options-dense
      use-input
    >
      <template v-if="data.model === 'User'" #option="scope">
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
      <template #append>
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          @navigate="router.push(linkTarget)"
          :linkable="data.link"
          :main-color="editColour"
          :main-icon="editIcon"
          :show-cancel="editOn && hasChanged"
          :show-link="!saving && !editOn"
          :show-main="data.editable && !saving"
          :show-spinner="saving"
          cancellable
        />
      </template>
    </q-select>
    <q-field v-if="data.dataType === 'BOOL'" :borderless="!editOn" :readonly="!editOn">
      <q-checkbox
        v-model="value"
        :disable="!editOn"
        :label="data.label"
        checked-icon="task_alt"
        unchecked-icon="highlight_off"
        left-label
      />
      <template #append>
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          @navigate="router.push(linkTarget)"
          :linkable="data.link"
          :main-color="editColour"
          :main-icon="editIcon"
          :show-cancel="editOn && hasChanged"
          :show-link="!saving && !editOn"
          :show-main="data.editable && !saving"
          :show-spinner="saving"
          cancellable
        />
      </template>
    </q-field>
    <div v-if="data.dataType === 'DATE'" class="field-date-container">
      <div class="field-date-wrapper">
        <div class="field-date-label q-field__label">
          <div>{{ data.label }}</div>
        </div>
        <DateChooser @changed="updateValue" :data="value" :editable="editOn" />
      </div>
      <div class="field-date-buttons">
        <EditButtons
          @action="onAction"
          @cancel="onCancel"
          :main-color="editColour"
          :main-icon="editIcon"
          :show-cancel="editOn && hasChanged"
          :show-main="data.editable && !saving"
          :show-spinner="saving"
          cancellable
        />
      </div>
    </div>
  </div>
</template>

<script>
import { snakeCase } from "change-case";
import { computed, defineComponent, onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";

import { requests } from "@/api";
import { DateChooser } from "@/components";
import { OptionListSchema } from "@/schemas";
import { useAPI } from "@/use";
import { nully } from "@/utils";

import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "ValueDisplay",
  components: { EditButtons, DateChooser },
  props: {
    data: {
      type: Object,
      required: true,
    },
    field: {
      type: String,
      required: true,
    },
  },
  emits: ["valueChanged"],

  setup(props, context) {
    const router = useRouter();
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const editOn = ref(false);
    const saving = ref(false);
    const ogValue = ref(null);
    const value = ref(null);
    const allOptions = ref([]);
    const options = ref([]);
    const loading = ref(false);
    const isNew = ref(!props.data.id || (props.data.value === null && props.data.show === true));

    const multiple = computed(() => Array.isArray(props.data.value));
    const hasChanged = computed(() => ogValue.value !== value.value);

    const model = computed(() =>
      props.data.model
        ? props.data.model === "Type"
          ? props.data.value.type
          : props.data.model
        : null,
    );

    const linkTarget = computed(() => {
      if (props.data.link) {
        const params = {};
        params[props.data.link] = props.data.value[props.data.link];
        return { name: model.value, params: params };
      } else {
        return null;
      }
    });

    const editIcon = computed(() =>
      editOn.value
        ? hasChanged.value
          ? "mdi-content-save-outline"
          : "mdi-close-circle-outline"
        : "mdi-cog-outline",
    );

    const editColour = computed(() =>
      editOn.value ? (hasChanged.value ? "green-6" : "orange-6") : "grey-5",
    );

    const getOptions = () => {
      return new Promise((resolve) => {
        const request = model.value
          ? requests.attributeTypes.getAttributeTypeOptions(
              snakeCase(props.field),
              true,
              model.value,
            )
          : requests.attributeTypes.getAttributeTypeOptions(snakeCase(props.field), true);
        fetchAPI(request).then(() => {
          if (success.value) {
            OptionListSchema.validate(data.value, { stripUnknown: false }).then((validated) => {
              resolve(validated);
            });
          }
        });
      });
    };

    const onAction = () => {
      if (editOn.value && hasChanged.value) {
        context.emit("valueChanged", {
          name: props.field,
          update: !isNew.value,
          source: props.data.source,
          id: props.data.id,
          value: value.value,
          oldValue: ogValue.value,
        });
      }
      editOn.value = !editOn.value;
    };

    const onCancel = () => {
      value.value = ogValue.value;
    };

    const optionsFilter = (val, update) => {
      if (val === "") {
        update(() => (options.value = allOptions.value));
        return;
      }
      update(() => {
        const needle = val.toLowerCase();
        options.value = allOptions.value.filter((v) => v.label.toLowerCase().indexOf(needle) > -1);
      });
    };

    const updateValue = (val) => {
      console.log("update VALUE", val);
      value.value = val;
    };

    onBeforeMount(() => {
      if (props.data.dataType === "FKEY") {
        loading.value = true;
        getOptions().then((result) => {
          allOptions.value = result;
          options.value = allOptions.value;
          ogValue.value = multiple.value
            ? Array.from(props.data.value, (v) => `${v.value.id}`)
            : `${props.data.value.id}`;
          value.value = ogValue.value;
          loading.value = false;
        });
      } else if (props.data.dataType === "DATE") {
        ogValue.value = props.data.value;
        value.value = ogValue.value;
      } else {
        ogValue.value = props.data.value;
        value.value = ogValue.value;
      }
    });

    return {
      editOn,
      value,
      options,
      onAction,
      router,
      linkTarget,
      multiple,
      loading,
      nully,
      optionsFilter,
      saving,
      hasChanged,
      onCancel,
      editIcon,
      editColour,
      updateValue,
    };
  },
});
</script>

<style lang="scss" scoped>
.value-display {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: baseline;
}
.value-display label {
  flex-grow: 1;
}
.field-date-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  border-bottom: 1px dotted rgba(0, 0, 0, 0.24);
  height: 56px;
}
.field-date-wrapper {
  display: flex;
  flex-direction: column;
}
.field-date-buttons {
  display: flex;
  margin-left: auto;
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
</style>
