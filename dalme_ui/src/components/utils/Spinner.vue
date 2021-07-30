<template>
  <div class="q-pa-lg">
    <q-inner-loading showing>
      <q-spinner color="primary" size="3em" :thickness="6" />
    </q-inner-loading>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Spinner",
});
</script>
