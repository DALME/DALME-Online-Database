<template>
  <div v-if="windowIndexShow">
    <div class="index-header">
      <div class="index-title">WINDOWS</div>
      <div class="index-btn-group">
        <q-btn icon="visibility_off" :disable="disableHideAll" @click.stop="hideAll" />
        <q-btn icon="visibility" :disable="disableShowAll" @click.stop="showAll" />
      </div>
    </div>

    <q-list>
      <q-item
        clickable
        class="q-px-sm q-py-none"
        :key="cuid"
        :class="{
          focussed: cuid === focus,
          pulse: !disabled && mouseoverSubmit && cuid === focus,
        }"
        v-for="(actor, cuid) in actors"
        @click.stop="() => handleFocus(cuid)"
      >
        <q-item-section side>
          <q-icon class="mode-icon" :name="editorModeIcons[actor.context.mode]" />
        </q-item-section>
        <q-item-section class="column">
          <div :class="actor.context.mode === 'create' ? 'row name text-capitalize' : 'row kind'">
            <span v-if="actor.context.mode === 'create'" class="q-mr-xs"> New </span>
            {{ actor.context.kind }}
          </div>
          <div v-if="actor.context.mode !== 'create'" class="row name text-grey-8">
            {{ actor.context.initialData.shortName }}
          </div>
        </q-item-section>
        <q-item-section side>
          <div class="row items-center">
            <q-icon
              class="q-mr-xs"
              v-if="!actor.context.visible"
              name="o_visibility_off"
              size="xs"
              color="grey-6"
            />
            <q-btn
              icon="center_focus_weak"
              @click.stop.stop="() => handleRecenter(cuid)"
              size="sm"
              class="text-orange-edit"
              unelevated
              round
            >
              <TooltipWidget self="center left">Recenter</TooltipWidget>
            </q-btn>
          </div>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
// eslint-disable-next-line unused-imports/no-unused-imports
import { all, keys, map as rMap, none, values } from "ramda";
import { defineComponent, ref } from "vue";
import { useActor } from "@xstate/vue";
import { useConstants, useEditing, useStores } from "@/use";
import { TooltipWidget } from "@/components";

export default defineComponent({
  name: "WindowIndex",
  components: {
    TooltipWidget,
  },
  setup() {
    const { editorModeIcons } = useConstants();
    const {
      disabled,
      focus,
      modals,
      hideAll,
      mouseoverSubmit,
      recenter,
      showAll,
      // eslint-disable-next-line unused-imports/no-unused-vars
      machine: { send, actorRef },
    } = useEditing();
    const { windowIndexShow } = useStores();
    const handleFocus = (cuid) => {
      const { send: actorSend } = useActor(modals.value[cuid].actor);
      send({ type: "SET_FOCUS", value: cuid });
      actorSend({ type: "SHOW" });
    };

    const handleRecenter = (cuid) => {
      handleFocus(cuid);
      recenter.value = cuid;
    };

    const actors = ref([]);
    const disableHideAll = ref(null);
    const disableShowAll = ref(null);

    actorRef.subscribe((snapshot) => {
      // console.log(snapshot);
      const modals = snapshot.context.modals;
      windowIndexShow.value = keys(modals).length > 0;
      // TODO: I'm sure all this can be optimized to only traverse once.
      actors.value = rMap(({ actor }) => useActor(actor).state, modals);
      // console.log(actors.value);
      const visibility = values(rMap((actor) => actor.context.visible, actors.value));
      disableHideAll.value = none(Boolean)(visibility);
      disableShowAll.value = all(Boolean)(visibility);
    });

    return {
      actors,
      disabled,
      disableHideAll,
      disableShowAll,
      focus,
      handleFocus,
      handleRecenter,
      hideAll,
      editorModeIcons,
      mouseoverSubmit,
      windowIndexShow,
      showAll,
    };
  },
});
</script>

<style lang="scss" scoped>
.index-header {
  width: 100%;
  display: flex;
  height: 27px;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #c87001;
  background: #ffca82;
  padding-left: 8px;
  box-shadow:
    1px 1px 0px 0px #ffffff4d inset,
    -1px -1px 0px 0px #5757573d inset;
}
.index-title {
  font-size: 12px;
  font-weight: 600;
  color: #a85e00;
}
.index-btn-group button {
  font-size: 10px;
  padding: 0 10px;
  height: 27px;
  border-radius: 0;
  border-left: 1px dotted #c87001;
  color: #a85e00;
}
.index-btn-group button::before {
  box-shadow: none;
}
.q-item {
  font-size: 12px;
  border-color: #d1d1d1;
  border-bottom-width: 1px;
  border-bottom-style: solid;
}
.kind {
  text-transform: capitalize;
  font-size: 10px;
  line-height: 10px;
}
.name {
  font-size: 12px;
  line-height: 14px;
  font-weight: 600;
  color: #616161;
}
.focussed {
  background-color: #fff3e0;
}
.focussed .mode-icon {
  color: #a85e00;
  font-weight: 600;
}
.text-orange-edit {
  color: #a85e00;
}
.pulse {
  background-color: #ffeaee;
}
.pulse .mode-icon {
  color: #ac0300;
  font-weight: 600;
}
</style>
