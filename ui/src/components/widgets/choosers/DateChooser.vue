<template>
  <div class="date-chooser-wrapper">
    <div v-if="!editable" class="date-chooser-text">{{ text }}</div>
    <div v-if="editable" class="date-chooser-input-container">
      <q-select
        v-model="day"
        @update:model-value="onChange"
        :options="dayOptions"
        class="date-chooser-field day"
        clearable
        dense
        options-dense
        outlined
      >
        <template #selected v-if="!day"><div class="select-placeholder">Day</div></template>
      </q-select>

      <q-select
        v-model="month"
        @update:model-value="onChange"
        :options="monthOptions"
        class="date-chooser-field month"
        clearable
        dense
        emit-value
        map-options
        options-dense
        outlined
      >
        <template #selected v-if="!month"><div class="select-placeholder">Month</div></template>
      </q-select>

      <q-input
        v-model="year"
        @update:model-value="onChange"
        class="date-chooser-field year"
        placeholder="Year"
        clearable
        dense
        outlined
      />

      <q-btn v-if="date" class="calendar-button" icon="event" dense flat>
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
        const newDate = new Date(newValue);
        day.value = newDate.getDay();
        month.value = newDate.getMonth();
        year.value = newDate.getFullYear();
      },
    });

    const text = computed(() => {
      if (date.value) {
        const dateObj = new Date(date.value);
        return formatDate(dateObj, "DATE_MED_WITH_WEEKDAY", "Europe/Paris");
      } else if (month.value && year.value) {
        const mOpt = monthOptions.find((x) => x.value === month.value);
        return `${mOpt.label}, ${year.value}`;
      } else if (year.value) {
        return year.value;
      } else {
        return "Invalid or missing date.";
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
.date-chooser-field {
  margin-right: 5px;
  font-size: 13px;
}
.date-chooser-field.day {
  min-width: 80px;
}
.date-chooser-field.month {
  min-width: 135px;
}
.date-chooser-field.year {
  min-width: 60px;
  max-width: 80px;
}
.select-placeholder {
  color: rgba(0, 0, 0, 0.6);
  font-size: 12px;
  line-height: 1.25;
  font-weight: 400;
  letter-spacing: 0.00937em;
}
.date-chooser-text {
  min-width: 80px;
}
:deep(.date-chooser-field .q-field__control),
:deep(.date-chooser-field .q-field__native) {
  min-height: 20px;
  height: 26px;
}
:deep(.date-chooser-field.q-select .q-field__control) {
  padding-right: 5px;
}
:deep(.date-chooser-field .q-field__native) {
  padding: 4px 0;
}
:deep(.date-chooser-field.q-field--outlined .q-field__control:before) {
  border: 1px solid rgba(0, 0, 0, 0.1);
}
:deep(.date-chooser-field .q-icon.q-field__focusable-action) {
  font-size: 14px;
}
:deep(.date-chooser-input-container .q-field__append) {
  height: auto;
}
.calendar-button {
  font-size: 11px;
  margin-right: 5px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  height: 26px;
  width: 26px;
  color: grey;
}
</style>
