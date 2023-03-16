<template>
  <div
    v-if="inlineIndexShow"
    class="container q-py-sm"
    :class="{
      focussed: isFocus,
      pulse: mouseoverSubmit && focus === 'inline',
    }"
    @click.stop="handleFocus"
  >
    <div class="q-pa-md q-gutter-sm row">
      <q-btn
        @click.stop="transport.undo"
        color="white"
        text-color="black"
        label="Undo"
        class="q-ml-auto"
      />
      <q-btn
        @click.stop="transport.redo"
        color="white"
        text-color="black"
        label="Redo"
        :disable="disableRedo"
      />
    </div>
    <q-list separator>
      <q-item v-for="entry in diffs" :key="entry.timestamp" class="column q-px-sm">
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
import { DateTime } from "luxon";
import { computed, defineComponent, watch } from "vue";
import { useEditing, useStores, useTransport } from "@/use";

export default defineComponent({
  name: "InlineIndex",
  setup() {
    const { transport } = useTransport();
    const {
      focus,
      mouseoverSubmit,
      machine: { send },
    } = useEditing();

    const diffs = computed(() => transport.history.value.slice(0, -1));
    const disableRedo = computed(() => (transport.canRedo.value ? false : true));
    const isFocus = computed(() => focus.value === "inline");
    const { inlineIndexShow } = useStores();
    const fromUnixTs = (unixTs) => DateTime.fromMillis(unixTs).toISO();
    const handleFocus = () => send("SET_FOCUS", { value: "inline" });

    watch(
      () => diffs.value,
      (newDiffs) => {
        inlineIndexShow.value = newDiffs.length > 0;
      },
    );

    return {
      diffs,
      disableRedo,
      focus,
      fromUnixTs,
      handleFocus,
      isFocus,
      mouseoverSubmit,
      inlineIndexShow,
      transport,
    };
  },
});
</script>

<style lang="scss">
.container {
  cursor: pointer;
}
.focussed {
  background: white;
  border-left: 4px solid green;
  transition: border-left 0.05s linear;
}
.pulse {
  border-left: 8px solid red;
  transition: border-left 0.5s linear;
}
.q-item {
  font-size: 12px;
}
</style>
