<template>
  <q-card v-if="!loading" :class="`chart-card q-pa-none ${orientation}`" bordered dense flat>
    <q-card-section class="q-pa-xs">
      <div class="text-subtitle2 text-center q-pa-sm">
        {{ title }}
      </div>
    </q-card-section>
    <q-separator class="full-width" />
    <q-card-section ref="chart-container" class="chart-container">
      <Bar v-if="chartType === 'bar'" :data="dataset" :options="options" :style="styles" />
      <Doughnut
        v-if="chartType === 'doughnut'"
        :data="dataset"
        :options="options"
        :style="styles"
      />
      <Line
        v-if="chartType === 'line'"
        id="dash-chart-container"
        :data="dataset"
        :options="options"
        :style="styles"
      />
      <Pie
        v-if="chartType === 'pie'"
        id="dash-chart-container"
        :data="dataset"
        :options="options"
        :style="styles"
      />
      <PolarArea v-if="chartType === 'polar'" :data="dataset" :options="options" :style="styles" />
      <Radar v-if="chartType === 'radar'" :data="dataset" :options="options" :style="styles" />
      <Bubble v-if="chartType === 'bubble'" :data="dataset" :options="options" :style="styles" />
      <Scatter v-if="chartType === 'scatter'" :data="dataset" :options="options" :style="styles" />
    </q-card-section>
    <q-card-actions class="chart-actions">
      <q-btn color="red" icon="favorite" flat round />
      <q-btn color="teal" icon="bookmark" flat round />
      <q-btn color="primary" icon="share" flat round />
    </q-card-actions>
  </q-card>
</template>

<script>
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  RadialLinearScale,
  Title,
  Tooltip,
} from "chart.js";
import { format } from "quasar";
import { computed, defineComponent, onMounted, ref } from "vue";
import { Bar, Bubble, Doughnut, Line, Pie, PolarArea, Radar, Scatter } from "vue-chartjs";

import { requests } from "@/api";
import { useAPI, useStores } from "@/use";

import { sampleOptions, samples } from "./sample-data.js";
import * as widgets from "./widgets";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  ArcElement,
  LineElement,
  RadialLinearScale,
  Filler,
);

export default defineComponent({
  name: "DashChartWidget",
  components: {
    Bar,
    Doughnut,
    // eslint-disable-next-line vue/no-reserved-component-names
    Line,
    Pie,
    PolarArea,
    Radar,
    Bubble,
    Scatter,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { capitalize } = format;
    const { ui } = useStores();
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const dataset = ref([]);
    const loading = ref(true);
    const options = ref({});
    const title = ref("");
    const chartType = ref("");

    const orientation = computed(() =>
      ["line", "bar", "bubble", "scatter"].includes(chartType.value) ? "horizontal" : "vertical",
    );

    const styles = computed(() => {
      const width =
        orientation.value === "horizontal"
          ? ui.windowWidth * 0.66 - 100
          : ui.windowWidth * 0.33 - 100;
      return {
        width: `${width}px`,
        "max-height": `${ui.windowHeight / 1.2 - 100}px`,
        position: "relative",
      };
    });

    const fetchData = (query, handler) => {
      return new Promise((resolve) => {
        fetchAPI(requests.datasets.get(query)).then(() => {
          if (success.value) {
            resolve(handler(data.value));
          }
        });
      });
    };

    onMounted(() => {
      if (props.name in widgets) {
        const widget = widgets[props.name];
        options.value = widget.options;
        title.value = widget.title;
        chartType.value = widget.type;
        fetchData(widget.query, widget.handler).then((result) => {
          dataset.value = result;
          console.log(result);
          loading.value = false;
        });
      } else {
        dataset.value = samples[props.name];
        options.value = sampleOptions[props.name] || { responsive: true };
        title.value = capitalize(`${props.name} chart`);
        chartType.value = props.name;
        loading.value = false;
      }
    });

    return {
      options,
      dataset,
      title,
      styles,
      orientation,
      loading,
      chartType,
    };
  },
});
</script>

<style lang="scss" scoped>
.chart-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  // width: calc(100vw * 0.33 - 200px) !important;
  // max-height: calc(100vh / 1.2);
}
.chart-card.horizontal {
  flex: 1 0 auto;
  // width: calc(100vw * 0.66 - 200px) !important;
}
// .chart-container {
//   display: flex;
//   flex-grow: 100;
//   flex-wrap: nowrap;
//   overflow: auto;
// }
.chart-actions {
  align-self: center;
  margin-top: auto;
}
</style>
