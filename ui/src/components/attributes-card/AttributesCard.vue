<template>
  <DetailCard :loading="loading" icon="mdi-view-list" title="Attributes" pad-container-list>
    <template #card-buttons>
      <q-btn
        v-if="!loading && attributeCandidates"
        :ripple="false"
        color="grey-5"
        icon="mdi-plus-circle-outline"
        size="sm"
        dense
        flat
        no-caps
      >
        <q-menu ref="attributes-menu" transition-hide="jump-up" transition-show="jump-down">
          <q-list bordered dense separator>
            <template v-for="attr in attributeCandidates" :key="attr.name">
              <q-item
                v-if="!creating.includes(attr.name)"
                :key="attr.name"
                @click="appendAttribute(attr)"
                clickable
                dense
              >
                <q-item-section>{{ attr.label }}</q-item-section>
              </q-item>
            </template>
          </q-list>
        </q-menu>
      </q-btn>
      <AdaptiveSpinner v-if="loading" class="q-mr-xs" color="green-6" size="14px" type="pie" />
    </template>
    <div v-if="!loading" ref="attributes-field" class="attributes-field">
      <template v-for="attr in attributes" :key="attr.name">
        <component
          :is="componentsByDataType[attr.dataType]"
          v-if="!exclusions.includes(attr.name)"
          :id="attr.id"
          @destroyed="onDestroyed"
          :description="attr.description"
          :label="attr.label"
          :repository="Attributes"
          field="value"
        />
      </template>
    </div>
  </DetailCard>
</template>

<script>
import { useSortBy } from "pinia-orm/helpers";
import { prop, sortBy } from "ramda";
import {
  computed,
  defineComponent,
  getCurrentInstance,
  h,
  onBeforeMount,
  ref,
  render,
  useTemplateRef,
} from "vue";

import { AdaptiveSpinner, DetailCard } from "@/components";
import { BooleanField, DateField, InputField, SelectField } from "@/components/fields";
import { Attributes } from "@/models";

export default defineComponent({
  name: "AttributesField",
  components: {
    AdaptiveSpinner,
    BooleanField,
    DetailCard,
    DateField,
    InputField,
    SelectField,
  },
  props: {
    repository: {
      type: Object,
      required: true,
    },
    id: {
      type: [Number, String],
      required: true,
    },
    exclusions: {
      type: Array,
      required: false,
      default: () => [],
    },
    order: {
      type: Array,
      required: false,
      default: () => [],
    },
    label: {
      type: String,
      required: false,
      default: "Attributes",
    },
    editable: {
      type: Boolean,
      required: false,
      default: true,
    },
  },

  setup(props) {
    const currentInstance = getCurrentInstance();
    const container = useTemplateRef("attributes-field");
    const menu = useTemplateRef("attributes-menu");
    const attributeTypes = ref([]);
    const contentType = ref(null);
    const loading = ref(false);
    const attributes = ref([]);
    const creating = ref([]);

    const componentsByDataType = {
      BOOL: BooleanField,
      DATE: DateField,
      FKEY: SelectField,
      FLOAT: InputField,
      INT: InputField,
      JSON: InputField,
      RREL: SelectField,
      STR: InputField,
    };

    const sortByLabel = sortBy(prop("label"));

    const attributeIds = computed(() => attributes.value.map((x) => x.attributeType));
    const attributeCandidates = computed(() => {
      if (!attributeTypes.value) return null;
      return sortByLabel(
        attributeTypes.value.filter(
          (x) =>
            !x.isLocal &&
            x.dataType !== "RREL" &&
            (!attributeIds.value.includes(x.id) || !x.isUnique),
        ),
      );
    });

    const appendAttribute = (attr) => {
      menu.value.hide();
      const newEl = document.createElement("div");
      const vnode = h(componentsByDataType[attr.dataType], {
        repository: Attributes,
        creating: true,
        defaults: {
          id: null,
          attributeType: attr.id,
          contentType: contentType.value,
          dataType: attr.dataType,
          description: attr.description,
          isUnique: attr.isUnique,
          label: attr.label,
          name: attr.name,
          objectId: props.id,
          value: null,
        },
        onDrop: () => onDrop(attr, newEl),
        onCreated: (nr) => onCreated(nr, newEl),
      });
      vnode.appContext = currentInstance.appContext.app._context;
      render(vnode, newEl);
      container.value.appendChild(newEl);
      if (attr.isUnique) creating.value.push(attr.name);
    };

    const onDrop = (attr, newEl) => {
      if (attr.isUnique) creating.value = creating.value.filter((x) => x !== attr.name);
      newEl.remove();
    };

    const onCreated = (newRecord, fieldEl) => {
      console.log("Attr oncreated", newRecord, creating.value);
      if (newRecord.isUnique) creating.value = creating.value.filter((x) => x !== newRecord.name);
      console.log("Attr oncreated removed creating", creating.value);
      attributes.value.push(newRecord);
      fieldEl.remove();
    };

    const onDestroyed = (id) => {
      console.log("Attr ondestroyed", id);
      attributes.value = attributes.value.filter((x) => x.id !== id);
    };

    onBeforeMount(() => {
      loading.value = true;
      props.repository.meta().then((meta) => {
        attributeTypes.value = meta.attributeTypes;
        contentType.value = meta.contentType;
        const attrs = Attributes.where("objectId", props.id).get();
        attributes.value = props.order
          ? useSortBy(attrs, (attr) => props.order.indexOf(attr.name))
          : attrs;
        loading.value = false;
      });
    });

    return {
      appendAttribute,
      attributeCandidates,
      attributeIds,
      Attributes,
      attributes,
      componentsByDataType,
      creating,
      loading,
      onDestroyed,
    };
  },
});
</script>
