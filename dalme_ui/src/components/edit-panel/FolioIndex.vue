<template>
  <div
    v-if="!isEmpty(folioList)"
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
        :clickable="folio.ref !== view.currentFolio"
        v-for="folio in folioList"
        :key="folio.id"
        class="column q-px-sm"
        @click.stop="eventBus.emit('changeFolio', folio.ref)"
      >
        <div>
          <code>{{ folio.name }}</code>
        </div>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { filter as rFilter, isEmpty } from "ramda";
import moment from "moment";
import { computed, defineComponent, watch } from "vue";
import { useEditing, useStores, useTransport } from "@/use";

export default defineComponent({
  name: "FolioIndex",
  setup() {
    const { transport } = useTransport();
    const {
      focus,
      mouseoverSubmit,
      machine: { send },
    } = useEditing();

    const disableRedo = computed(() =>
      transport.canRedo.value ? false : true,
    );
    const isFocus = computed(() => focus.value === "inline");
    const { view, editPanel, eventBus } = useStores();
    const fromUnixTs = (unixTs) =>
      moment.unix(unixTs / 1000).format("YYYY-MM-DD HH:mm:ss");

    const folioList = computed(() => {
      if ("folios" in view.value) {
        return rFilter((folio) => folio.editOn, view.value.folios);
      } else {
        return null;
      }
    });

    const handleFocus = () => send("SET_FOCUS", { value: "inline" });

    watch(folioList, () => {
      editPanel.value.folioIndexShow = !isEmpty(folioList.value);
    });

    return {
      disableRedo,
      eventBus,
      focus,
      fromUnixTs,
      handleFocus,
      isEmpty,
      isFocus,
      mouseoverSubmit,
      editPanel,
      transport,
      view,
      folioList,
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
