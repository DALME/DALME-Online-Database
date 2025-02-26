<template>
  <div
    v-if="!nully(pageList)"
    class="container q-py-sm"
    :class="{
      focussed: isFocus,
      pulse: mouseoverSubmit && focus === 'inline',
    }"
    @click.stop="handleFocus"
  >
    <div class="index-header">
      <div class="index-title">FOLIOS</div>
    </div>
    <q-list separator>
      <q-item
        :clickable="page.ref !== view.currentPageRef"
        v-for="page in pageList"
        :key="page.id"
        class="column q-px-sm"
        @click.stop="eventBus.emit('changePage', page.ref)"
      >
        <div>
          <code>{{ page.name }}</code>
        </div>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { filter as rFilter } from "ramda";
import { computed, defineComponent, watch } from "vue";
import { useEditing, useEventHandling, useStores, useTransport } from "@/use";
import { nully } from "@/utils";

export default defineComponent({
  name: "PageIndex",
  setup() {
    const { transport } = useTransport();
    const {
      focus,
      mouseoverSubmit,
      machine: { send },
    } = useEditing();

    const disableRedo = computed(() => (transport.canRedo.value ? false : true));
    const isFocus = computed(() => focus.value === "inline");
    const { pageIndexShow, pageCount, view } = useStores();
    const { eventBus } = useEventHandling();

    const pageList = computed(() => {
      if (pageCount.value) {
        return rFilter((page) => page.editOn, view.value.pages);
      } else {
        return null;
      }
    });

    const handleFocus = () => send({ type: "SET_FOCUS", value: "inline" });

    watch(pageList, () => {
      pageIndexShow.value = !nully(pageList.value);
    });

    return {
      disableRedo,
      eventBus,
      focus,
      handleFocus,
      nully,
      isFocus,
      mouseoverSubmit,
      transport,
      pageList,
      view,
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
