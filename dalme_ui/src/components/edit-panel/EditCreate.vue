<template>
  <q-fab
    icon="add"
    text-color="black"
    direction="up"
    :color="dragging ? 'grey' : 'amber'"
    :disable="dragging"
  >
    <q-fab
      padding="0.5rem"
      icon="bookmark"
      text-color="black"
      direction="left"
      :color="dragging ? 'grey' : 'orange'"
      :disable="dragging"
    >
      <q-fab-action
        :onClick="() => handleClick('archive')"
        color="amber"
        text-color="black"
        icon="villa"
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Archive
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('record')"
        color="amber"
        text-color="black"
        icon="format_list_numbered"
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Record
        </Tooltip>
      </q-fab-action>
    </q-fab>

    <q-fab-action
      :onclick="() => handleClick('set')"
      color="amber"
      text-color="black"
      icon="collections_bookmark"
      disabled
    >
      <Tooltip anchor="center left" self="center right" :offset="[10, 10]">
        Create Set
      </Tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('task')"
      color="amber"
      text-color="black"
      icon="assignment"
    >
      <Tooltip anchor="center left" self="center right" :offset="[10, 10]">
        Create Task
      </Tooltip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('ticket')"
      color="amber"
      text-color="black"
      icon="task"
      disabled
    >
      <Tooltip anchor="center left" self="center right" :offset="[10, 10]">
        Create Ticket
      </Tooltip>
    </q-fab-action>
  </q-fab>
</template>

<script>
import cuid from "cuid";
import { defineAsyncComponent, defineComponent, inject } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditCreate",
  components: {
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  setup() {
    const mode = "create";
    const {
      machine: { send },
    } = useEditing();

    const dragging = inject("dragging");

    const handleClick = (kind) =>
      send("SPAWN_FORM", {
        cuid: cuid(),
        key: null,
        kind,
        mode,
        initialData: {},
      });

    return {
      dragging,
      handleClick,
    };
  },
});
</script>
