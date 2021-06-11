<template>
  <q-card class="q-ma-md">
    <q-item>
      <q-item-section avatar>
        <q-avatar icon="attachment"> </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label class="text-subtitle1"> Attachments </q-item-label>
      </q-item-section>
    </q-item>

    <q-card-section>
      <q-img :src="attachment.source"></q-img>
      <div class="row">
        <q-space />
        <div class="q-pa-sm">
          {{ attachment.filename }}
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, inject } from "vue";

export default defineComponent({
  name: "Attachments",
  setup() {
    const attachment = inject("attachment");
    return { attachment };
  },
});
</script>
