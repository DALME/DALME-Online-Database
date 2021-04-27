<template>
  <div class="spinner">
    <spring-spinner :animation-duration="5000" :size="30" :color="'#000'" />
  </div>
</template>

<script>
import { SpringSpinner } from "epic-spinners";

export default {
  name: "Spinner",
  components: {
    SpringSpinner,
  },
};
</script>

<style scoped>
.spinner {
  display: flex;
  height: 100%;
  justify-content: center;
  margin: 5rem auto 0 auto;
  padding: 1rem;
}
</style>
