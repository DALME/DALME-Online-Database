<template>
  <SuspenseWithError>
    <template #default>
      <Tickets />
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
import { Tickets } from "@/components";
import { Spinner, SuspenseWithError } from "@/components/utils";

export default {
  name: "Dashboard",
  components: {
    Spinner,
    SuspenseWithError,
    Tickets,
  },
};
</script>

<style scoped></style>
