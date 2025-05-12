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
      <slot name="card-buttons" />
    </q-item>
    <q-separator class="bg-grey-4" />
    <q-card-section :class="bodyClasses">
      <slot>{{ noData }}</slot>
    </q-card-section>
  </q-card>
</template>

<script>
import { computed, defineComponent, provide, ref } from "vue";

export default defineComponent({
  name: "DetailCard",
  props: {
    icon: {
      type: String,
      required: false,
      default: "mdi-information-box",
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
    padContainerList: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const cardFilter = ref("");
    const bodyClasses = computed(() => {
      if (props.padContainer) return "q-pa-md";
      if (props.padContainerList) return "q-px-md q-pb-md q-pt-xs";
      return "q-pa-none";
    });

    provide("cardFilter", cardFilter);

    return {
      cardFilter,
      bodyClasses,
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
</style>
