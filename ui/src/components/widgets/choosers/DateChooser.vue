<template>
  <div class="date-chooser-wrapper">
    <div v-if="!editable" class="date-chooser-text">{{ text }}</div>
    <div v-if="editable" class="date-chooser-input-container q-ml-lg">
      <q-select
        v-model="day"
        @update:model-value="onChange"
        :options="dayOptions"
        class="date-chooser-day"
        label="Day"
        borderless
        dense
        options-dense
      />
      <q-select
        v-model="month"
        @update:model-value="onChange"
        :options="monthOptions"
        class="date-chooser-month"
        label="Month"
        borderless
        dense
        map-options
        options-dense
      />
      <q-input
        v-model="year"
        @update:model-value="onChange"
        class="date-chooser-year"
        label="Year"
        borderless
        dense
      />
      <q-btn v-if="date" class="q-mx-sm" icon="event" size="sm" dense flat>
        <q-popup-proxy cover>
          <q-date v-model="date" @update:model-value="onChange" mask="YYYY-MM-DD" minimal />
        </q-popup-proxy>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { range } from "ramda";
import { computed, defineComponent, onBeforeMount, ref, watch } from "vue";

import { formatDate } from "@/utils";

export default defineComponent({
  name: "DateChooser",
  props: {
    data: {
      type: Object,
      required: true,
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["changed"],
  setup(props, ctx) {
    const day = ref(null);
    const month = ref(null);
    const year = ref(null);

    const date = computed({
      get() {
        if (day.value && month.value && year.value) {
          const d = day.value.toString().padStart(2, "0");
          const m = month.value.toString().padStart(2, "0");
          return `${year.value}-${m}-${d}`;
        } else {
          return null;
        }
      },
      set(newValue) {
        const date = new Date(newValue);
        day.value = date.day;
        month.value = date.month;
        year.value = date.year;
      },
    });

    const text = computed(() => {
      if (date.value) {
        const dateObj = new Date(date.value, { zone: "Europe/Paris" });
        return formatDate(dateObj, "DATE_MED_WITH_WEEKDAY");
      } else {
        return "TEXT";
      }
    });

    const dayOptions = range(1, 32);

    const monthOptions = [
      { label: "January", value: 1 },
      { label: "February", value: 2 },
      { label: "March", value: 3 },
      { label: "April", value: 4 },
      { label: "May", value: 5 },
      { label: "June", value: 6 },
      { label: "July", value: 7 },
      { label: "August", value: 8 },
      { label: "September", value: 9 },
      { label: "October", value: 10 },
      { label: "November", value: 11 },
      { label: "December", value: 12 },
    ];

    const onChange = () => {
      ctx.emit("changed", {
        day: day.value,
        month: month.value,
        year: year.value,
      });
    };

    watch(
      () => props.data,
      (newData) => {
        day.value = newData.day;
        month.value = newData.month;
        year.value = newData.year;
      },
    );

    onBeforeMount(() => {
      day.value = props.data.day;
      month.value = props.data.month;
      year.value = props.data.year;
    });

    return {
      day,
      month,
      year,
      date,
      text,
      dayOptions,
      monthOptions,
      onChange,
    };
  },
});
</script>

<style lang="scss" scoped>
.date-chooser-wrapper {
  display: flex;
  align-items: center;
  flex-direction: row;
}
.date-chooser-input-container {
  display: flex;
  align-items: center;
  flex-direction: row;
}
.date-chooser-day {
  min-width: 50px;
}
.date-chooser-month {
  min-width: 100px;
}
.date-chooser-year {
  min-width: 60px;
}
</style>
