<template>
  <div class="q-ma-md full-width full-height" @on-loaded="skeleton = false">
    <template v-if="skeleton">
      <IssueTrackerSkeleton />
    </template>
    <template v-else>
      <div class="row">
        <div class="column">
          <q-card class="q-ma-md">
            <q-item>
              <q-item-section avatar>
                <q-avatar icon="assignment"> </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label class="text-h5">
                  <slot name="title"></slot>
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-card-section>
              <slot name="description"></slot>
            </q-card-section>
          </q-card>

          <!-- TODO: IssueComments -->
        </div>

        <q-card class="q-ml-sm">
          <slot name="actions"></slot>
        </q-card>
      </div>
    </template>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

import IssueTrackerSkeleton from "./IssueTrackerSkeleton.vue";

export default defineComponent({
  name: "IssueTracker",
  components: {
    IssueTrackerSkeleton,
  },
  setup() {
    const skeleton = ref(true);

    return {
      skeleton,
    };
  },
});
</script>
