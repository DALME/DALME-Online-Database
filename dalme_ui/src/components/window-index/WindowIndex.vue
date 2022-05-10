<template>
  <div v-if="show" class="q-py-sm">
    <div class="q-pa-md q-gutter-sm row">
      <q-btn
        class="q-ml-auto"
        color="white"
        label="Hide All"
        text-color="black"
        :disable="disableHideAll"
        @click.stop="hideAll"
      />
      <q-btn
        color="white"
        label="Show All"
        text-color="black"
        :disable="disableShowAll"
        @click.stop="showAll"
      />
    </div>

    <q-list separator>
      <q-item
        clickable
        class="column q-px-sm"
        :key="cuid"
        :class="{
          focussed: cuid === focus,
          pulse: !disabled && mouseoverSubmit && cuid === focus,
        }"
        v-for="(actor, cuid) in actors"
        v-ripple:blue-3
        @click.stop="() => handleFocus(cuid)"
      >
        <div>
          <div class="row items-center">
            <span class="text-caption text-grey">
              <code>{{ cuid }}</code>
            </span>
          </div>

          <div class="row text-subtitle1 text-capitalize text-bold q-mt-xs">
            <div>
              {{ actor.context.mode }}
              {{ actor.context.kind }}
            </div>

            <div class="q-ml-auto items-center row">
              <q-icon
                class="q-mr-sm"
                v-if="!actor.context.visible"
                name="visibility_off"
                size="xs"
              />

              <q-btn
                icon="center_focus_weak"
                @click.stop.stop="() => handleRecenter(cuid)"
                size="8px"
                round
              >
                <Tooltip self="center left">Recenter</Tooltip>
              </q-btn>
            </div>
          </div>
        </div>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { all, keys, map as rMap, none, values } from "ramda";
import { defineAsyncComponent, defineComponent, inject, ref } from "vue";
import { useActor } from "@xstate/vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "WindowIndex",
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup() {
    const {
      disabled,
      focus,
      modals,
      hideAll,
      mouseoverSubmit,
      recenter,
      showAll,
      machine: { send, service },
    } = useEditing();

    const show = inject("windowIndexShow");

    const handleFocus = (cuid) => {
      const { send: actorSend } = useActor(modals.value[cuid].actor);
      send("SET_FOCUS", { value: cuid });
      actorSend("SHOW");
    };
    const handleRecenter = (cuid) => {
      handleFocus(cuid);
      recenter.value = cuid;
    };

    const actors = ref([]);
    const disableHideAll = ref(null);
    const disableShowAll = ref(null);
    service.onTransition(({ context: { modals } }) => {
      show.value = keys(modals).length > 0;
      // TODO: I'm sure all this can be optimized to only traverse once.
      actors.value = rMap(({ actor }) => useActor(actor).state, modals);
      const visibility = values(
        rMap((actor) => actor.context.visible, actors.value),
      );
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
      mouseoverSubmit,
      show,
      showAll,
    };
  },
});
</script>

<style lang="scss" scoped>
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
