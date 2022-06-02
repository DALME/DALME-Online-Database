<template>
  <div v-if="!loading">
    <q-card>
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="bookmark" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-weight-medium">Source</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">Type</div>
          <div class="col-8">{{ source.type.name }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">Name</div>
          <div class="col-8">{{ source.name }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">
            Short name
          </div>
          <div class="col-8">{{ source.shortName }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">List</div>
          <div class="col-8">
            <q-icon :name="source.hasInventory ? 'done' : 'close'" />
          </div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">Owner</div>
          <div class="col-8">
            <router-link
              :to="{
                name: 'User',
                params: { username: source.owner.username },
              }"
            >
              {{ source.owner.fullName }}
            </router-link>
          </div>
        </div>

        <div class="row q-mt-xs" v-if="source.parent">
          <div class="col-2 text-weight-medium text-right q-mr-lg">Parent</div>
          <div class="col-8">
            <router-link
              :to="{
                name: 'Source',
                params: { id: source.parent.id },
              }"
            >
              {{ source.parent.name }}
            </router-link>
          </div>
        </div>

        <div class="row q-mt-xs" v-if="source.primaryDataset">
          <div class="col-2 text-weight-medium text-right q-mr-lg">
            Primary Dataset
          </div>
          <div class="col-8">
            <router-link
              :to="{
                name: 'Set',
                params: { id: source.primaryDataset.id },
              }"
            >
              {{ source.primaryDataset.name }}
            </router-link>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="q-mt-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="assignment" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-weight-medium"> Attributes </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section v-if="!hasAttributes">
        <div class="q-mt-xs text-center">
          <p>No attributes assigned.</p>
        </div>
      </q-card-section>
      <q-card-section v-else>
        <template v-for="(attribute, idx) in attributes" :key="idx">
          <template v-if="!isNil(attribute.value)">
            <div class="row q-mt-xs">
              <div class="col-2 text-weight-medium text-right q-mr-lg">
                {{ getAttributeLabel(attribute.key) }}
              </div>
              <div v-if="attribute.key === 'url'">
                <a :href="attribute.value" target="_blank">
                  {{ attribute.value }}
                </a>
              </div>
              <div v-else-if="Array.isArray(attribute.value)" class="col-8">
                {{ attribute.value[0].name }}
              </div>
              <div v-else-if="isObj(attribute.value)" class="col-8">
                {{ attribute.value.name }}
              </div>
              <div v-else class="col-8">
                {{ attribute.value }}
              </div>
            </div>
          </template>
        </template>
      </q-card-section>
    </q-card>

    <q-card class="q-mt-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="info" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-weight-medium"> Metadata </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">ID</div>
          <div class="col-8">{{ source.id }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-2 text-weight-medium text-right q-mr-lg">Created</div>
          <div class="col-8">
            <router-link
              :to="{
                name: 'User',
                params: { username: source.created.username },
              }"
            >
              {{ source.created.user }}
            </router-link>
          </div>
        </div>

        <div class="row q-mt-xs" v-if="source.workflow">
          <div class="col-2 text-weight-medium text-right q-mr-lg">
            Modified
          </div>
          <div class="col-8">
            <span>{{ source.modified.timestamp }} by </span>
            <router-link
              :to="{
                params: { username: source.modified.username },
              }"
            >
              {{ source.modified.user }}
            </router-link>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <q-card class="q-mt-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="subject" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-weight-medium"> Description </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section v-if="!hasDescription">
        <div class="q-mt-xs text-center text-body1">
          <p>No description assigned.</p>
        </div>
      </q-card-section>
      <q-card-section v-else>
        <div class="q-mt-xs text-left text-body1">
          {{ source.attributes.description }}
        </div>
      </q-card-section>
    </q-card>

    <q-card v-if="hasChildren" class="q-mt-md">
      <SourceChildren :children="source.children" />
    </q-card>

    <q-card v-if="hasPages" class="q-mt-md">
      <SourcePages :pages="source.pages" />
    </q-card>

    <q-card v-if="hasAgents" class="q-mt-md">
      <SourceAgents :agents="source.agents" />
    </q-card>

    <q-card v-if="hasPlaces" class="q-mt-md">
      <SourcePlaces :places="source.places" />
    </q-card>

    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { filter as rFilter, isEmpty, isNil, map } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { computedInject } from "@vueuse/core";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { sourceDetailSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

import SourceAgents from "./SourceAgents.vue";
import SourceChildren from "./SourceChildren.vue";
import SourcePages from "./SourcePages.vue";
import SourcePlaces from "./SourcePlaces.vue";

const getAttributeLabel = (attribute) => {
  return {
    url: "Web Address",
    mk1Identifier: "Mk.I ID",
    mk2Identifier: "Mk.II ID",
    altIdentifier: "Alt ID",
    archivalSeries: "Archival Series",
    archivalNumber: "Archival Number",
    recordType: "Record Type",
    language: "Language",
    recordTypePhrase: "Record Type Phrase",
    namedPersons: "Named Persons",
    decscription: "Description",
    debtPhrase: "Debt Phrase",
    debtAmount: "Debt Amount",
    debtUnit: "Debt Unit",
    debtSource: "Debt Source",
    date: "Date",
    startDate: "Start Date",
    endDate: "End Date",
    locale: "Locale",
    defaultRights: "Default Rights",
    authority: "Authority",
    format: "Format",
    support: "Support",
    zoteroKey: "Zotero Key",
  }[attribute];
};

const isObj = (obj) => {
  const type = typeof obj;
  return type === "function" || (type === "object" && !!obj);
};

const notNully = (value) => !isNil(value) && !isEmpty(value);

export default defineComponent({
  name: "SourceDetail",
  components: {
    SourceAgents,
    SourceChildren,
    SourcePages,
    SourcePlaces,
    OpaqueSpinner,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();

    const { loading, success, data, fetchAPI } = apiInterface();
    const source = ref({});

    const id = inject("id");

    // TODO: Could use a transducer at some point.
    const attributes = computed(() =>
      rFilter(
        (attribute) => !["description"].includes(attribute.key),
        map(
          (key) => ({ key, value: source.value.attributes[key] }),
          Object.keys(source.value.attributes).reverse(),
        ),
      ),
    );
    const hasAttributes = computed(() => !isNil(source.value.attributes));
    const hasDescription = computed(
      () => !isNil(source.value.attributes.description),
    );
    const hasAgents = computed(() => notNully(source.value.agents));
    const hasChildren = computed(() => notNully(source.value.children));
    const hasPlaces = computed(() => notNully(source.value.places));
    const hasPages = computedInject("hasPages", (injected) => {
      injected.value = notNully(source.value.pages);
      return notNully(source.value.pages);
    });

    provide("model", "Source");

    useMeta(() => ({
      title: source.value ? source.value.name : `Source ${id.value}`,
    }));

    const fetchData = async () => {
      await fetchAPI(requests.sources.getSource(id.value));
      if (success.value)
        await sourceDetailSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            resource.value =
              {
                archive: "archive",
                "file unit": "archivalFile",
                record: "record",
              }[value.type.name.toLowerCase()] || "bibliography";
            source.value = value;
            loading.value = false;
          });
    };

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          id.value = to;
          await fetchData();
        }
      },
      { immediate: true },
    );

    editingDetailRouteGuard();

    return {
      attributes,
      getAttributeLabel,
      hasAgents,
      hasAttributes,
      hasChildren,
      hasDescription,
      hasPages,
      hasPlaces,
      isObj,
      isNil,
      loading,
      source,
    };
  },
});
</script>
