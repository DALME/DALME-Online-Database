<template>
  <div v-if="show" class="q-py-sm">
    <div class="q-pa-md q-gutter-sm row">
      <q-btn
        color="white"
        text-color="black"
        label="Hide All"
        class="q-ml-auto"
        @click="hideAll"
      />
      <q-btn
        color="white"
        text-color="black"
        label="Show All"
        @click="showAll"
      />
    </div>
    <q-list separator>
      <q-item
        clickable
        v-for="(actor, cuid) in actors"
        :key="cuid"
        :class="{
          focussed: cuid === focus,
          pulse: !disabled && mouseoverSubmit && cuid === focus,
        }"
        @click="() => handleFocus(cuid)"
        v-ripple:blue-3
        class="column q-px-sm"
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
                @click.stop="() => handleRecenter(cuid)"
                size="8px"
                round
              >
                <q-tooltip self="center left">Recenter</q-tooltip>
              </q-btn>
            </div>
          </div>
        </div>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { keys, map as rMap } from "ramda";
import { defineComponent, inject, ref, watch } from "vue";
import { useActor } from "@xstate/vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "WindowIndex",
  setup() {
    const {
      disabled,
      focus,
      forms,
      hideAll,
      mouseoverSubmit,
      recenter,
      showAll,
      machine: { send, state },
    } = useEditing();

    const actors = ref([]);
    const show = inject("windowIndexShow");

    const handleFocus = (cuid) => {
      const { send: actorSend } = useActor(forms.value[cuid]);
      send("SET_FOCUS", { value: cuid });
      actorSend("SHOW");
    };
    const handleRecenter = (cuid) => {
      handleFocus(cuid);
      recenter.value = cuid;
    };

    watch(
      () => state.value,
      (newState) => {
        show.value = keys(newState.context.forms).length > 0;
        actors.value = rMap(
          (actor) => useActor(actor).state,
          newState.context.forms,
        );
      },
    );

    return {
      actors,
      disabled,
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
