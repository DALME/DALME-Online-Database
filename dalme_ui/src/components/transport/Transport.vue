<template>
  <q-drawer
    side="right"
    v-model="show"
    show-if-above
    bordered
    :breakpoint="500"
    class="bg-grey-3"
  >
    <q-scroll-area class="fit">
      <div class="q-pa-sm">
        <div class="q-pa-md q-gutter-sm row">
          <q-btn
            @click="transport.undo"
            color="white"
            text-color="black"
            label="Undo"
            class="q-ml-auto"
          />
          <q-btn
            @click="transport.redo"
            color="white"
            text-color="black"
            label="Redo"
            :disable="disableRedo"
          />
        </div>
        <q-list separator>
          <q-item
            v-for="entry in diffs"
            :key="entry.timestamp"
            class="column q-px-xs"
          >
            <div>
              <code>{{ entry.snapshot }}</code>
            </div>
            <div class="q-pt-xs q-ml-auto">
              <code>{{ fromUnixTs(entry.timestamp) }}</code>
            </div>
          </q-item>
        </q-list>
      </div>
    </q-scroll-area>
  </q-drawer>
</template>

<script>
import moment from "moment";
import { isEmpty } from "ramda";
import { computed, defineComponent, inject } from "vue";

export default defineComponent({
  name: "Transport",
  setup() {
    const transport = inject("transport");
    const show = computed({
      get: () => !isEmpty(transport),
      set: () => !isEmpty(transport),
    });
    const diffs = computed(() => transport.history.value.slice(0, -1));
    const disableRedo = computed(() =>
      transport.canRedo.value ? false : true,
    );
    const fromUnixTs = (unixTs) =>
      moment.unix(unixTs / 1000).format("YYYY-MM-DD HH:mm:ss");

    return {
      disableRedo,
      fromUnixTs,
      transport,
      diffs,
      show,
    };
  },
});
</script>

<style lang="scss">
.q-item {
  font-size: 12px;
}
</style>
