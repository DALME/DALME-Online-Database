<template>
  <q-card flat bordered class="detail-card">
    <q-item dense class="q-pb-none q-px-sm bg-grey-2 text-grey-7">
      <q-item-section v-if="icon" side class="q-pr-sm">
        <q-icon :name="icon" color="grey-6" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label class="text-subtitle2">
          {{ title }}
          <q-badge
            v-if="badgeValue"
            rounded
            color="purple-4"
            align="middle"
            label="badgeValue"
          />
        </q-item-label>
      </q-item-section>
      <template v-if="showFilter">
        <q-input
          dense
          borderless
          hide-bottom-space
          v-model="cardFilter"
          debounce="300"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="Filter"
          class="card-title-search"
          color="blue-9"
        >
          <template v-slot:append>
            <q-icon
              v-if="cardFilter === ''"
              name="search"
              color="blue-grey-5"
              size="14px"
            />
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
    </q-item>
    <q-separator class="bg-grey-4" />
    <q-card-section :class="padContainer ? 'q-pa-md' : 'q-pa-none'">
      <slot>
        {{ noData }}
      </slot>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, provide, ref } from "vue";

export default defineComponent({
  name: "DetailCard",
  props: {
    icon: {
      type: String,
      required: false,
    },
    title: {
      type: String,
      required: true,
    },
    noData: {
      type: String,
      required: false,
      default: "There is no data to show.",
    },
    badgeValue: {
      type: Number,
      required: false,
    },
    showFilter: {
      type: Boolean,
      required: false,
      default: false,
    },
    padContainer: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  setup() {
    const cardFilter = ref("");
    provide("cardFilter", cardFilter);
    return { cardFilter };
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
</style>
