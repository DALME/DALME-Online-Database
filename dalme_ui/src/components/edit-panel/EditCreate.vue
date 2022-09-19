<template>
  <q-fab
    icon="add"
    text-color="black"
    direction="up"
    :color="dragging ? 'grey' : 'amber'"
    :disable="dragging"
    push
  >
    <q-fab
      padding="0.5rem"
      icon="bookmark"
      text-color="black"
      direction="left"
      :color="dragging ? 'grey' : 'orange'"
      :disable="dragging"
      push
    >
      <q-fab-action
        :onClick="() => handleClick('archive')"
        color="amber"
        text-color="black"
        icon="villa"
        push
      >
        <Tooltip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Archive
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('archivalFile')"
        color="amber"
        text-color="black"
        icon="inventory"
        push
      >
        <Tooltip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Archival File
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('bibliography')"
        color="amber"
        text-color="black"
        icon="library_books"
        push
      >
        <Tooltip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Bibliography
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('record')"
        color="amber"
        text-color="black"
        icon="format_list_numbered"
        push
      >
        <Tooltip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Record
        </Tooltip>
      </q-fab-action>
    </q-fab>

    <q-fab
      padding="0.5rem"
      icon="collections_bookmark"
      text-color="black"
      direction="left"
      :color="dragging ? 'grey' : 'orange'"
      :disable="dragging"
      push
    >
      <q-fab-action
        :onclick="() => handleClick('corpus')"
        color="amber"
        text-color="black"
        icon="local_library"
        push
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Corpus
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('collection')"
        color="amber"
        text-color="black"
        icon="apps"
        push
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Collection
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('dataset')"
        color="amber"
        text-color="black"
        icon="schema"
        push
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Dataset
        </Tooltip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('workset')"
        color="amber"
        text-color="black"
        icon="work"
        push
      >
        <Tooltip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Workset
        </Tooltip>
      </q-fab-action>
    </q-fab>

    <q-fab-action
      :onclick="() => handleClick('task')"
      color="amber"
      text-color="black"
      icon="assignment"
      push
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
      push
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
