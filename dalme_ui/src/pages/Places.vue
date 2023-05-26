<template>
  <PageContainer>
    <PlaceList />
  </PageContainer>
</template>

<script>
import { useMeta } from "quasar";
import { defineComponent } from "vue";
import { PageContainer, PlaceList } from "@/components";

export default defineComponent({
  name: "PlacesPageContainer",
  components: {
    PageContainer,
    PlaceList,
  },
  setup() {
    useMeta({ title: "Places" });
  },
});
</script>
