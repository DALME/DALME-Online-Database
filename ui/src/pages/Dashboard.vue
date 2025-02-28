<template>
  <PageContainer class="main-max-width">
    <div class="row horizontal-stretch q-gutter-sm dash-container">
      <DashChartWidget name="polar" />
      <DashChartWidget name="RecordTypes" />
      <DashChartWidget name="radar" />
      <DashChartWidget name="doughnut" />
      <DashChartWidget name="pie" />
      <DashChartWidget name="line" />
      <DashChartWidget name="bubble" />
      <DashChartWidget name="scatter" />
    </div>
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { DashChartWidget, PageContainer } from "@/components";

export default defineComponent({
  name: "DashBoard",
  components: {
    DashChartWidget,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Dashboard" });
    const query = {
      target: "Record",
      cat1: "record_type",
    };

    return { query };
  },
});
</script>

<style lang="scss">
.dash-container {
  margin-top: 10px;
}
.viz-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 40px;
  padding: 30px 20px;
}
</style>
