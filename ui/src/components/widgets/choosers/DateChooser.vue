<template>
  <div class="date-chooser-wrapper">
    <div v-if="!editable" class="date-chooser-text">{{ text }}</div>
    <div v-if="editable" class="date-chooser-input-container q-ml-lg">
      <q-select
        v-model="day"
        :options="dayOptions"
        label="Day"
        @update:model-value="onChange"
        options-dense
        dense
        borderless
        class="date-chooser-day"
      />
      <q-select
        v-model="month"
        :options="monthOptions"
        label="Month"
        @update:model-value="onChange"
        map-options
        options-dense
        dense
        borderless
        class="date-chooser-month"
      />
      <q-input
        v-model="year"
        label="Year"
        @update:model-value="onChange"
        dense
        borderless
        class="date-chooser-year"
      />
      <q-btn v-if="date" icon="event" size="sm" dense flat class="q-mx-sm">
        <q-popup-proxy cover>
          <q-date v-model="date" minimal mask="YYYY-MM-DD" @update:model-value="onChange" />
        </q-popup-proxy>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, ref, onBeforeMount, watch } from "vue";
import { range } from "ramda";
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
