<template>
  <div v-if="!loading" class="value-display">
    <q-input
      v-if="data.dataType === 'STR'"
      :borderless="!editOn"
      :readonly="!editOn"
      v-model="value"
      :label="data.label"
      :placeholder="data.description ? data.description : null"
    >
      <template v-slot:append>
        <EditButtons
          :linkable="data.link"
          cancellable
          :main-icon="editIcon"
          :main-color="editColour"
          :show-main="data.editable && !saving"
          :show-cancel="editOn && hasChanged"
          :show-spinner="saving"
          :show-link="!saving && !editOn"
          @navigate="router.push(linkTarget)"
          @action="onAction"
          @cancel="onCancel"
        />
      </template>
    </q-input>
    <q-select
      v-if="data.dataType === 'FKEY'"
      :multiple="multiple"
      :use-chips="multiple"
      :borderless="!editOn"
      :readonly="!editOn"
      v-model="value"
      :options="options"
      :label="data.label"
      hide-dropdown-icon
      map-options
      options-dense
      use-input
      emit-value
      menu-shrink
      input-debounce="0"
      @filter="optionsFilter"
    >
      <template v-if="data.model === 'User'" v-slot:option="scope">
        <q-item v-bind="scope.itemProps" dense>
          <q-item-section side>
            <q-avatar v-if="!nully(scope.opt.icon)" size="34px">
              <q-img :src="scope.opt.icon" class="chooser-avatar-image" fit="cover" ratio="1" />
            </q-avatar>
            <q-icon v-else size="34px" name="mdi-account-circle" color="grey-4" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ scope.opt.label }}</q-item-label>
            <q-item-label caption>{{ scope.opt.detail }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>
      <template v-slot:append>
        <EditButtons
          :linkable="data.link"
          cancellable
          :main-icon="editIcon"
          :main-color="editColour"
          :show-main="data.editable && !saving"
          :show-cancel="editOn && hasChanged"
          :show-spinner="saving"
          :show-link="!saving && !editOn"
          @navigate="router.push(linkTarget)"
          @action="onAction"
          @cancel="onCancel"
        />
      </template>
    </q-select>
    <q-field
      v-if="data.dataType === 'BOOL'"
      :borderless="!editOn"
      :readonly="!editOn"
      :label="data.label"
      stack-label
    >
      <q-toggle :disable="!editOn" v-model="value" color="green" />
      <template v-slot:append>
        <EditButtons
          :linkable="data.link"
          cancellable
          :main-icon="editIcon"
          :main-color="editColour"
          :show-main="data.editable && !saving"
          :show-cancel="editOn && hasChanged"
          :show-spinner="saving"
          :show-link="!saving && !editOn"
          @navigate="router.push(linkTarget)"
          @action="onAction"
          @cancel="onCancel"
        />
      </template>
    </q-field>
  </div>
</template>

<script>
import { computed, defineComponent, ref, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import { useAPI } from "@/use";
import { requests } from "@/api";
import { OptionListSchema } from "@/schemas";
import { snakeCase } from "change-case";
import { nully } from "@/utils";
import EditButtons from "./EditButtons.vue";

export default defineComponent({
  name: "ValueDisplay",
  props: {
    data: {
      type: Object,
      required: true,
    },
    field: String,
  },
  emits: ["valueChanged"],
  components: { EditButtons },

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
    };
  },
});
</script>

<style lang="scss" scoped>
.value-display {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.value-display label {
  flex-grow: 1;
}
@media only screen and (min-width: 1100px) {
  .value-display {
    width: 49%;
    border-bottom: 1px dotted #d8d8d8;
    border-right: 1px dotted #d8d8d8;
  }
}
</style>
