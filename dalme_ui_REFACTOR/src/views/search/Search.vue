<template>
  <SuspenseWithError>
    <template #default>
      <h1>Stubbed</h1>
    </template>
    <template #fallback>
      <Spinner />
    </template>
    <template #error>
      <h1>Failed to load</h1>
    </template>
  </SuspenseWithError>
</template>

<script>
import { Spinner, SuspenseWithError } from "@/components/utils";

export default {
  name: "Search",
  components: {
    Spinner,
    SuspenseWithError,
  },
};
</script>

<style scoped></style>
