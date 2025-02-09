<template>
  <q-card :class="`chart-card q-pa-none ${chartType}`" flat dense bordered>
    <q-card-section class="q-pa-xs">
      <div class="text-subtitle2 text-center q-pa-sm">
        {{ title }}
      </div>
    </q-card-section>
    <q-separator class="full-width" />
    <q-card-section class="chart-container" ref="chart-container">
      <Bar v-if="chartType === 'bar'" :options="options" :data="data" :style="styles" />
      <Doughnut v-if="chartType === 'doughnut'" :options="options" :data="data" :style="styles" />
      <Line
        v-if="chartType === 'line'"
        id="dash-chart-container"
        :options="options"
        :data="data"
        :style="styles"
      />
      <Pie
        v-if="chartType === 'pie'"
        id="dash-chart-container"
        :options="options"
        :data="data"
        :style="styles"
      />
      <PolarArea v-if="chartType === 'polar'" :options="options" :data="data" :style="styles" />
      <Radar v-if="chartType === 'radar'" :options="options" :data="data" :style="styles" />
      <Bubble v-if="chartType === 'bubble'" :options="options" :data="data" :style="styles" />
      <Scatter v-if="chartType === 'scatter'" :options="options" :data="data" :style="styles" />
    </q-card-section>
    <q-card-actions class="chart-actions">
      <q-btn flat round color="red" icon="favorite" />
      <q-btn flat round color="teal" icon="bookmark" />
      <q-btn flat round color="primary" icon="share" />
    </q-card-actions>
  </q-card>
</template>

<script>
import { computed, defineComponent, useTemplateRef } from "vue";
import { Bar, Doughnut, Line, Pie, PolarArea, Radar, Bubble, Scatter } from "vue-chartjs";
import {
  Chart as ChartJS,
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
} from "chart.js";
import { format } from "quasar";

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
  name: "DashChart",
  props: {
    chartType: {
      type: String,
      required: true,
    },
  },
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
  setup(props) {
    const { capitalize } = format;
    const container = useTemplateRef("chart-container");
    const options = computed(() => {
      let base = { responsive: true };
      if (props.chartType in baseOptions) {
        base = { ...base, ...baseOptions[props.chartType] };
      }
      return base;
    });

    const data = computed(() => {
      return store[props.chartType];
    });

    const styles = computed(() => {
      if (!container.value) return;
      console.log("styles", container.value.$el.offsetWidth);
      return {
        // width: `${container.value.$el.offsetWidth}px`,
        height: `${container.value.$el.offsetHeight}px`,
        position: "relative",
      };
    });

    const title = computed(() => capitalize(`${props.chartType} chart`));

    const store = {
      bar: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
          {
            label: "Bar Dataset",
            barPercentage: 0.5,
            barThickness: 6,
            maxBarThickness: 8,
            minBarLength: 2,
            data: [10, 20, 30, 40, 50, 60, 70],
          },
        ],
      },
      doughnut: {
        labels: ["Red", "Blue", "Yellow"],
        datasets: [
          {
            label: "Doughnut Dataset",
            data: [300, 50, 100],
            backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"],
            hoverOffset: 4,
          },
        ],
      },
      line: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
          {
            label: "Line Dataset",
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
          },
        ],
      },
      pie: {
        labels: ["A", "B", "C"],
        datasets: [
          {
            label: "Pie Dataset",
            data: [200, 500, 50],
            backgroundColor: ["rgb(99, 255, 132)", "rgb(162, 52, 235)", "rgb(255, 20, 205)"],
            hoverOffset: 4,
          },
        ],
      },
      polar: {
        labels: ["Red", "Green", "Yellow", "Grey", "Blue"],
        datasets: [
          {
            label: "Polar Area Dataset",
            data: [11, 16, 7, 3, 14],
            backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(75, 192, 192)",
              "rgb(255, 205, 86)",
              "rgb(201, 203, 207)",
              "rgb(54, 162, 235)",
            ],
          },
        ],
      },
      radar: {
        labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
        datasets: [
          {
            label: "Radar Dataset 1",
            data: [65, 59, 90, 81, 56, 55, 40],
            fill: true,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgb(255, 99, 132)",
            pointBackgroundColor: "rgb(255, 99, 132)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgb(255, 99, 132)",
          },
          {
            label: "Radar Dataset 2",
            data: [28, 48, 40, 19, 96, 27, 100],
            fill: true,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgb(54, 162, 235)",
            pointBackgroundColor: "rgb(54, 162, 235)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgb(54, 162, 235)",
          },
        ],
      },
      scatter: {
        datasets: [
          {
            label: "Scatter Dataset",
            data: [
              {
                x: -10,
                y: 0,
              },
              {
                x: 0,
                y: 10,
              },
              {
                x: 10,
                y: 5,
              },
              {
                x: 0.5,
                y: 5.5,
              },
            ],
            backgroundColor: "rgb(255, 99, 132)",
          },
        ],
      },
      bubble: {
        datasets: [
          {
            label: "BubbleDataset",
            data: [
              {
                x: 20,
                y: 30,
                r: 15,
              },
              {
                x: 40,
                y: 10,
                r: 10,
              },
            ],
            backgroundColor: "rgb(255, 99, 132)",
          },
        ],
      },
    };

    const baseOptions = {
      bar: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
      radar: {
        elements: {
          line: {
            borderWidth: 3,
          },
        },
      },
      scatter: {
        scales: {
          x: {
            type: "linear",
            position: "bottom",
          },
        },
      },
    };

    return {
      options,
      data,
      title,
      styles,
    };
  },
});
</script>

<style lang="scss">
.chart-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  // max-width: calc(100vw / 2) !important;
  max-height: calc(100vh / 1.5);
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
