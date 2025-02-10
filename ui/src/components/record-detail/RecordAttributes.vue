<template>
  <div v-if="record" class="row q-pt-md">
    <div class="col-9 q-pr-md">
      <DetailCard icon="bookmark" title="Record" padContainer>
        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Name</div>
          <div class="col-8">{{ record.name }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Short name</div>
          <div class="col-8">{{ record.shortName }}</div>
        </div>

        <div class="row q-mt-xs">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Type</div>
          <div class="col-8">
            <q-chip
              v-if="record.hasInventory"
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
                params: { username: record.owner.username },
              }"
            >
              {{ record.owner.fullName }}
            </router-link>
            <q-chip
              v-if="record.isPrivate"
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

        <div class="row q-mt-xs" v-if="record.parent">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Parent</div>
          <div class="col-8">
            <router-link
              class="text-link"
              :to="{
                name: 'Record',
                params: { id: record.parent.id },
              }"
            >
              {{ record.parent.name }}
            </router-link>
          </div>
        </div>

        <div class="row q-mt-xs" v-if="record.primaryDataset">
          <div class="col-3 text-weight-medium text-right q-mr-lg">Primary Dataset</div>
          <div class="col-8">
            <router-link
              class="text-link"
              :to="{
                name: 'Set',
                params: { id: record.primaryDataset.id },
              }"
            >
              {{ record.primaryDataset.name }}
            </router-link>
            <br />
            <span class="text-caption text-grey-8">
              {{ record.primaryDataset.detailString }}
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
        <MarkdownEditor v-if="hasDescription" :text="record.attributes.description" />
      </DetailCard>

      <DetailCard v-if="hasPages" icon="auto_stories" title="Folios" showFilter class="q-mt-md">
        <RecordPages overview :pages="record.pages" />
      </DetailCard>

      <DetailCard
        v-if="hasChildren"
        icon="account_tree"
        title="Children"
        showFilter
        class="q-mt-md"
      >
        <RecordChildren overview :children="record.children" />
      </DetailCard>

      <DetailCard v-if="hasAgents" icon="people" title="Agents" showFilter class="q-mt-md">
        <RecordAgents overview :agents="record.agents" />
      </DetailCard>

      <DetailCard v-if="hasPlaces" icon="place" title="Places" showFilter class="q-mt-md">
        <RecordPlaces overview :places="record.places" />
      </DetailCard>
    </div>

    <div class="col-3 q-pl-md">
      <template v-for="(attr, label) in attributes" :key="label">
        <template v-if="!isNil(attr) && label !== 'Description'">
          <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">
            {{ label }}
          </div>
          <template v-if="attr.length > 1">
            <div
              v-if="isObject(attr[0].value)"
              class="text-13"
              v-text="attr.map((x) => x.value.label || x.value.name).join(', ')"
            />
            <div v-else class="text-13" v-text="attr.map((x) => x.value).join(', ')" />
          </template>
          <template v-else>
            <div v-if="isObject(attr[0].value)" class="text-13">
              {{ attr[0].value.label || attr[0].value.name }}
            </div>
            <div v-else class="text-13">
              <BooleanValue
                v-if="attr[0].dataType === 'BOOL'"
                :value="attr[0].value"
                trueIcon="check_circle"
              />
              <span v-else>{{ attr[0].value }}</span>
            </div>
          </template>
        </template>
        <q-separator class="q-my-md" />
      </template>
      <div class="text-detail text-grey-8 text-weight-bold q-mb-sm">Unique Id</div>
      <div class="q-mb-sm text-13">{{ record.id }}</div>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, inject, onMounted } from "vue";
import { isNil, groupBy, prop } from "ramda";
import { BooleanValue, DetailCard, MarkdownEditor } from "@/components";
import RecordAgents from "./RecordAgents.vue";
import RecordChildren from "./RecordChildren.vue";
import RecordPages from "./RecordPages.vue";
import RecordPlaces from "./RecordPlaces.vue";
import { isObject } from "@/utils";

export default defineComponent({
  name: "RecordAttributes",
  components: {
    BooleanValue,
    DetailCard,
    MarkdownEditor,
    RecordAgents,
    RecordChildren,
    RecordPages,
    RecordPlaces,
  },
  setup() {
    const record = inject("record");
    const hasAttributes = inject("hasAttributes");
    const hasPages = inject("hasPages");
    const hasChildren = inject("hasChildren");
    const hasAgents = inject("hasAgents");
    const hasPlaces = inject("hasPlaces");

    const hasDescription = computed(() => !isNil(record.value.attributes.description));

    const attributes = computed(() => {
      return groupBy(prop("label"), record.value.attributes);
    });

    onMounted(() => {
      console.log("RecordAttributes", attributes.value);
    });

    return {
      attributes,
      hasAttributes,
      hasAgents,
      hasChildren,
      hasDescription,
      hasPages,
      hasPlaces,
      isObject,
      isNil,
      record,
    };
  },
});
</script>
