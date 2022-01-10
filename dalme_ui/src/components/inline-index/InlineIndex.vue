<template>
  <div
    v-if="show"
    class="container q-py-sm"
    :class="{ focussed: isFocus }"
    @click="handleFocus"
  >
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
        class="column q-px-sm"
      >
        <div>
          <code>{{ entry.snapshot }}</code>
        </div>
        <div class="q-pt-sm q-ml-auto">
          <span class="text-caption text-grey">
            <code>{{ fromUnixTs(entry.timestamp) }}</code>
          </span>
        </div>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import moment from "moment";
import { computed, defineComponent, inject, watch } from "vue";

import { useEditing, useTransport } from "@/use";

export default defineComponent({
  name: "Transport",
  setup() {
    const { transport } = useTransport();
    const {
      machine: { send },
      focus,
    } = useEditing();

    const diffs = computed(() => transport.history.value.slice(0, -1));
    const disableRedo = computed(() =>
      transport.canRedo.value ? false : true,
    );
    const isFocus = computed(() => focus.value === "inline");

    const show = inject("inlineIndexShow");

    const fromUnixTs = (unixTs) =>
      moment.unix(unixTs / 1000).format("YYYY-MM-DD HH:mm:ss");

    const handleFocus = () => send("SET_FOCUS", { value: "inline" });

    watch(
      () => diffs.value,
      (newDiffs) => {
        show.value = newDiffs.length > 0;
      },
    );

    return {
      diffs,
      disableRedo,
      fromUnixTs,
      handleFocus,
      isFocus,
      show,
      transport,
    };
  },
});
</script>

<style lang="scss" scoped>
.container {
  cursor: pointer;
}
.focussed {
  background: white;
  border-left: 4px solid green;
}
.q-item {
  font-size: 12px;
}
</style>
