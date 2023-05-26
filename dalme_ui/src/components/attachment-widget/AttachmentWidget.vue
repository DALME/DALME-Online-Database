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
      <q-img :src="attachment.source">
        <template v-slot:loading>
          <q-spinner />
        </template>

        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            Couldn't load attachment
          </div>
        </template>

        <div class="absolute-bottom-right text-subtitle1 text-center">
          <a
            :href="attachment.source"
            target="_blank"
            class="q-pa-sm text-white"
          >
            {{ attachment.filename }}
          </a>
        </div>
      </q-img>
    </q-card-section>
    <OpaqueSpinner :showing="!attachment" />
  </q-card>
</template>

<script>
import { defineComponent, inject } from "vue";

import { OpaqueSpinner } from "@/components/utils";

export default defineComponent({
  name: "AttachmentWidget",
  components: {
    OpaqueSpinner,
  },
  setup() {
    const attachment = inject("attachment");
    return { attachment };
  },
});
</script>
