<template>
  <div class="row q-pt-md">
    <div class="col-9 q-pr-md">
      <DetailCard icon="bookmark" title="Source" padContainer>
        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Name</div>
          <div class="col-8">{{ source.name }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">
            Short name
          </div>
          <div class="col-8">{{ source.shortName }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Type</div>
          <div class="col-8">
            {{ source.type.name }}
            <q-chip
              v-if="source.hasInventory"
              dense
              size="10px"
              outline
              color="green-9"
              class="text-bold"
            >
              LIST
            </q-chip>
          </div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Owner</div>
          <div class="col-8">
            <router-link
              class="text-link"
              :to="{
                name: 'User',
                params: { username: source.owner.username },
              }"
            >
              {{ source.owner.fullName }}
            </router-link>
            <q-chip
              v-if="source.isPrivate"
              dense
              size="10px"
              outline
              color="red-10"
              class="q-ml-sm text-bold"
            >
              PRIVATE
            </q-chip>
          </div>
        </div>

        <div class="row q-mt-xs" v-if="source.parent">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Parent</div>
          <div class="col-8">
            <router-link
              class="text-link"
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
          <div class="col-3 text-weight-medium text-right q-mr-lg">
            Primary Dataset
          </div>
          <div class="col-8">
            <router-link
              class="text-link"
              :to="{
                name: 'Set',
                params: { id: source.primaryDataset.id },
              }"
            >
              {{ source.primaryDataset.name }}
            </router-link>
            <br />
            <span class="text-caption text-grey-8">
              {{ source.primaryDataset.detailString }}
            </span>
          </div>
        </div>
      </DetailCard>

      <DetailCard
        icon="subject"
        title="Description"
        noData="No description assigned."
        padContainer
        class="q-mt-md"
      >
        <MarkdownEditor
          v-if="hasDescription"
          :text="source.attributes.description"
        />
      </DetailCard>

      <DetailCard
        v-if="hasPages"
        icon="auto_stories"
        title="Folios"
        showFilter
        class="q-mt-md"
      >
        <SourcePages overview :pages="source.pages" />
      </DetailCard>

      <DetailCard
        v-if="hasChildren"
        icon="account_tree"
        title="Children"
        showFilter
        class="q-mt-md"
      >
        <SourceChildren overview :children="source.children" />
      </DetailCard>

      <DetailCard
        v-if="hasAgents"
        icon="people"
        title="Agents"
        showFilter
        class="q-mt-md"
      >
        <SourceAgents overview :agents="source.agents" />
      </DetailCard>

      <DetailCard
        v-if="hasPlaces"
        icon="place"
        title="Places"
        showFilter
        class="q-mt-md"
      >
        <SourcePlaces overview :places="source.places" />
      </DetailCard>
    </div>

    <div class="col-3 q-pl-md">
      <template v-for="(value, name) in source.attributes" :key="name">
        <template v-if="!isNil(value) && name !== 'description'">
          <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
            {{ getAttributeLabel(name) }}
          </div>
          <div v-if="name === 'url'" class="text-13">
            <a :href="value" target="_blank">{{ value }}</a>
          </div>
          <div v-else-if="Array.isArray(value)" class="text-13">
            {{ value[0].name }}
          </div>
          <div v-else-if="isObj(value)" class="text-13">
            {{ value.name }}
          </div>
          <div v-else class="text-13">
            {{ value }}
          </div>
          <q-separator class="q-my-md" />
        </template>
      </template>
      <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
        Unique Id
      </div>
      <div class="q-mb-sm text-13">{{ source.id }}</div>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, inject } from "vue";
import { filter as rFilter, isNil, map } from "ramda";
import { DetailCard, MarkdownEditor } from "@/components";
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
    description: "Description",
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

export default defineComponent({
  name: "SourceAttributes",
  components: {
    DetailCard,
    MarkdownEditor,
    SourceAgents,
    SourceChildren,
    SourcePages,
    SourcePlaces,
  },
  setup() {
    const source = inject("source");
    const hasAttributes = inject("hasAttributes");
    const hasPages = inject("hasPages");
    const hasChildren = inject("hasChildren");
    const hasAgents = inject("hasAgents");
    const hasPlaces = inject("hasPlaces");

    const hasDescription = computed(
      () => !isNil(source.value.attributes.description),
    );

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

    return {
      attributes,
      getAttributeLabel,
      hasAttributes,
      hasAgents,
      hasChildren,
      hasDescription,
      hasPages,
      hasPlaces,
      isObj,
      isNil,
      source,
    };
  },
});
</script>
