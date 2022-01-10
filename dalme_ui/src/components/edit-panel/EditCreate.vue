<template>
  <q-fab
    icon="add"
    text-color="black"
    direction="up"
    :color="disabled ? 'grey' : 'amber'"
    :disable="disabled"
  >
    <q-fab-action
      :onClick="() => handleClick('source')"
      color="amber"
      text-color="black"
      icon="bookmark"
    >
      <q-tooltip
        class="bg-blue"
        transition-show="scale"
        transition-hide="scale"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create source
      </q-tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('set')"
      color="amber"
      text-color="black"
      icon="collections_bookmark"
    >
      <q-tooltip
        class="bg-blue"
        transition-show="scale"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create set
      </q-tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('task')"
      color="amber"
      text-color="black"
      icon="assignment"
    >
      <q-tooltip
        class="bg-blue"
        transition-show="scale"
        transition-hide="scale"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create task
      </q-tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('ticket')"
      color="amber"
      text-color="black"
      icon="subject"
    >
      <q-tooltip
        class="bg-blue"
        transition-show="scale"
        transition-hide="scale"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create ticket
      </q-tooltip>
    </q-fab-action>
  </q-fab>
</template>

<script>
import cuid from "cuid";
import { defineComponent } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditCreate",
  setup() {
    const mode = "create";
    const {
      machine: { send },
    } = useEditing();

    const handleClick = (kind) =>
      send("SPAWN_FORM", { cuid: cuid(), kind, mode });

    return {
      disabled: false,
      handleClick,
    };
  },
});
</script>
