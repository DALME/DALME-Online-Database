<template>
  <div
    v-if="notNully(folioList)"
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
        :clickable="folio.ref !== view.currentFolioRef"
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
import { filter as rFilter } from "ramda";
import moment from "moment";
import { computed, defineComponent, watch } from "vue";
import { useEditing, useEventHandling, useStores, useTransport } from "@/use";
import { notNully } from "@/components/utils";

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
    const { folioIndexShow, folioCount, view } = useStores();
    const { eventBus } = useEventHandling();
    const fromUnixTs = (unixTs) =>
      moment.unix(unixTs / 1000).format("YYYY-MM-DD HH:mm:ss");

    const folioList = computed(() => {
      if (folioCount.value) {
        return rFilter((folio) => folio.editOn, view.value.folios);
      } else {
        return null;
      }
    });

    const handleFocus = () => send("SET_FOCUS", { value: "inline" });

    watch(folioList, () => {
      folioIndexShow.value = notNully(folioList.value);
    });

    return {
      disableRedo,
      eventBus,
      focus,
      fromUnixTs,
      handleFocus,
      notNully,
      isFocus,
      mouseoverSubmit,
      transport,
      folioList,
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
