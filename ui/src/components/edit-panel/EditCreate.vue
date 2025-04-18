<template>
  <q-fab ref="cFab" direction="down" icon="data_saver_on" square>
    <q-fab
      :hide-label="false"
      color="orange"
      direction="left"
      icon="bookmark"
      label="Record"
      label-position="right"
      padding="0.5rem"
      text-color="black"
      external-label
    >
      <q-fab-action
        :on-click="() => handleClick('archive')"
        color="amber"
        icon="villa"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="bottom middle" self="bottom middle">
          Create Archive
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :on-click="() => handleClick('archivalFile')"
        color="amber"
        icon="inventory"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="bottom middle" self="bottom middle">
          Create Archival File
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :on-click="() => handleClick('bibliography')"
        color="amber"
        icon="library_books"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="bottom middle" self="bottom middle">
          Create Bibliography
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :on-click="() => handleClick('record')"
        color="amber"
        icon="format_list_numbered"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="bottom middle" self="bottom middle">
          Create Record
        </ToolTip>
      </q-fab-action>
    </q-fab>

    <q-fab
      color="orange"
      direction="left"
      icon="collections_bookmark"
      padding="0.5rem"
      text-color="black"
    >
      <q-fab-action
        :onclick="() => handleClick('corpus')"
        color="amber"
        icon="local_library"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="top middle" self="top middle"> Create Corpus </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('collection')"
        color="amber"
        icon="apps"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="top middle" self="top middle">
          Create Collection
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('dataset')"
        color="amber"
        icon="schema"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="top middle" self="top middle"> Create Dataset </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('workset')"
        color="amber"
        icon="work"
        text-color="black"
        push
      >
        <ToolTip :offset="[0, 35]" anchor="top middle" self="top middle"> Create Workset </ToolTip>
      </q-fab-action>
    </q-fab>

    <q-fab-action
      :onclick="() => handleClick('task')"
      color="amber"
      icon="assignment"
      text-color="black"
      push
    >
      <ToolTip :offset="[10, 10]" anchor="center left" self="center right"> Create Task </ToolTip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('ticket')"
      color="amber"
      icon="task"
      text-color="black"
      push
    >
      <ToolTip :offset="[10, 10]" anchor="center left" self="center right"> Create Ticket </ToolTip>
    </q-fab-action>
  </q-fab>
</template>

<script>
import { createId as cuid } from "@paralleldrive/cuid2";
import { defineComponent, ref } from "vue";

import { ToolTip } from "@/components";
import { useEditing } from "@/use";

export default defineComponent({
  name: "EditCreate",
  components: {
    ToolTip,
  },
  setup() {
    const mode = "create";
    const cFab = ref(null);
    const {
      machine: { send },
    } = useEditing();

    const handleClick = (kind) => {
      cFab.value.hide();
      send({ type: "SPAWN_FORM", cuid: cuid(), key: null, kind, mode, initialData: {} });
    };

    return {
      cFab,
      handleClick,
    };
  },
});
</script>
