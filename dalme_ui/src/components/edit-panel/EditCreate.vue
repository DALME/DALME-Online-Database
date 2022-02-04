<template>
  <q-fab
    icon="add"
    text-color="black"
    direction="up"
    :color="disabled ? 'grey' : 'amber'"
    :disable="disabled"
  >
    <q-fab
      padding="0.5rem"
      icon="bookmark"
      text-color="black"
      direction="left"
      :color="disabled ? 'grey' : 'orange'"
      :disable="disabled"
    >
      <q-fab-action
        :onClick="() => handleClick('record')"
        color="amber"
        text-color="black"
        icon="bookmark"
      >
        <q-tooltip
          class="bg-blue"
          anchor="top middle"
          self="top middle"
          :offset="[0, 35]"
        >
          Create Record
        </q-tooltip>
      </q-fab-action>
    </q-fab>

    <q-fab-action
      :onclick="() => handleClick('set')"
      color="amber"
      text-color="black"
      icon="collections_bookmark"
      disabled
    >
      <q-tooltip
        class="bg-blue"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create Set
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
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create Task
      </q-tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('ticket')"
      color="amber"
      text-color="black"
      icon="task"
      disabled
    >
      <q-tooltip
        class="bg-blue"
        anchor="center left"
        self="center right"
        :offset="[10, 10]"
      >
        Create Ticket
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
      send("SPAWN_FORM", { cuid: cuid(), kind, mode, initialData: {} });

    return {
      disabled: false,
      handleClick,
    };
  },
});
</script>
