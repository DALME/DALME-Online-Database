<template>
  <PageContainer class="main-max-width">
    <div class="row horizontal-stretch q-gutter-sm dash-container">
      <DashChart chart-type="polar" />
      <DashChart chart-type="line" class="col-grow" />
      <DashChart chart-type="radar" />
      <DashChart chart-type="doughnut" />
      <DashChart chart-type="pie" />
      <DashChart chart-type="bubble" class="col-grow" />
      <DashChart chart-type="scatter" class="col-grow" />
      <DashChart chart-type="bar" class="col-grow" />
    </div>
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { DashChart, PageContainer } from "@/components";

export default defineComponent({
  name: "DashBoard",
  components: {
    DashChart,
    PageContainer,
  },
  setup() {
    useMeta({ title: "Dashboard" });
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
