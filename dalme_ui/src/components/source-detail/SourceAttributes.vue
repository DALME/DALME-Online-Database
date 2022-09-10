<template>
  <div class="row q-pt-md">
    <div class="col-12 col-md-6 q-pr-md">
      <q-card flat bordered class="detail-card">
        <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
          <q-item-section side class="q-pr-sm">
            <q-icon name="bookmark" color="indigo-5" size="xs" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-subtitle2">Source</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="bg-indigo-3" />

        <q-card-section>
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
            <div class="col-3 text-weight-medium text-right q-mr-lg">
              Parent
            </div>
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
            <div class="col-3 text-weight-medium text-right q-mr-lg">
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
              <br />
              <span class="text-caption text-grey-8">
                {{ source.primaryDataset.detailString }}
              </span>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="detail-card q-mt-md">
        <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
          <q-item-section side class="q-pr-sm">
            <q-icon name="subject" color="indigo-5" size="xs" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-subtitle2"> Description </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="bg-indigo-5" />

        <q-card-section v-if="!hasDescription">
          No description assigned.
        </q-card-section>

        <q-card-section v-else>
          <MarkdownEditor :text="source.attributes.description" />
        </q-card-section>
      </q-card>

      <q-card v-if="hasPages" flat bordered class="detail-card q-mt-md">
        <SourcePages overview :pages="source.pages" />
      </q-card>

      <q-card flat bordered class="detail-card q-mt-md">
        <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
          <q-item-section side class="q-pr-sm">
            <q-icon name="info" color="indigo-5" size="xs" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-subtitle2"> Metadata </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="bg-indigo-5" />

        <q-card-section>
          <div class="row q-mt-xs">
            <div class="col-3 text-weight-medium text-right q-mr-lg">ID</div>
            <div class="col-8">{{ source.id }}</div>
          </div>

          <div class="row q-mt-xs">
            <div class="col-3 text-weight-medium text-right q-mr-lg">
              Created
            </div>
            <div class="col-8">
              <span>{{ source.created.timestamp }} by </span>
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
            <div class="col-3 text-weight-medium text-right q-mr-lg">
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
    </div>
    <div class="col-12 col-md-6">
      <q-card flat bordered class="detail-card">
        <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
          <q-item-section side class="q-pr-sm">
            <q-icon name="assignment" color="indigo-5" size="xs" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-subtitle2"> Attributes </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="bg-indigo-5" />

        <q-card-section v-if="!hasAttributes">
          <div class="row q-mt-xs">
            <div class="col-3 q-mr-lg" />
            <div class="col-8">No attributes assigned.</div>
          </div>
        </q-card-section>
        <q-card-section v-else>
          <template v-for="(attribute, idx) in attributes" :key="idx">
            <template v-if="!isNil(attribute.value)">
              <div class="row q-mt-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
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

      <q-card v-if="hasChildren" flat bordered class="detail-card q-mt-md">
        <SourceChildren overview :children="source.children" />
      </q-card>

      <q-card v-if="hasAgents" flat bordered class="detail-card q-mt-md">
        <SourceAgents overview :agents="source.agents" />
      </q-card>

      <q-card v-if="hasPlaces" flat bordered class="detail-card q-mt-md">
        <SourcePlaces overview :places="source.places" />
      </q-card>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, inject } from "vue";
import { filter as rFilter, isNil, map } from "ramda";
import MarkdownEditor from "../markdown-editor/MarkdownEditor.vue";
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

<style scoped lang="scss">
.detail-card {
  border-color: #9fa8da;
}
</style>
