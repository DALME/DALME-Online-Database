<template>
  <div class="row">
    <div class="column">
      <q-card>
        <q-item>
          <q-item-section avatar>
            <q-avatar icon="assignment"> </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-h5">
              <q-skeleton width="30rem" />
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator />

        <q-card-section>
          <q-skeleton height="10rem" square />
        </q-card-section>
      </q-card>

      <!-- TODO: IssueCommentsSkeleton -->
    </div>

    <q-card class="q-ml-sm">
      <q-skeleton height="100%" square />
    </q-card>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "IssueTrackerSkeleton",
});
</script>
