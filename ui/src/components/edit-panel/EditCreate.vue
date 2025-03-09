<template>
  <q-fab ref="cFab" icon="data_saver_on" direction="down" square>
    <q-fab
      padding="0.5rem"
      icon="bookmark"
      label="Record"
      external-label
      label-position="right"
      text-color="black"
      direction="left"
      color="orange"
      :hide-label="false"
    >
      <q-fab-action
        :onClick="() => handleClick('archive')"
        color="amber"
        text-color="black"
        icon="villa"
        push
      >
        <ToolTip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Archive
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('archivalFile')"
        color="amber"
        text-color="black"
        icon="inventory"
        push
      >
        <ToolTip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Archival File
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('bibliography')"
        color="amber"
        text-color="black"
        icon="library_books"
        push
      >
        <ToolTip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Bibliography
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onClick="() => handleClick('record')"
        color="amber"
        text-color="black"
        icon="format_list_numbered"
        push
      >
        <ToolTip anchor="bottom middle" self="bottom middle" :offset="[0, 35]">
          Create Record
        </ToolTip>
      </q-fab-action>
    </q-fab>

    <q-fab
      padding="0.5rem"
      icon="collections_bookmark"
      text-color="black"
      direction="left"
      color="orange"
    >
      <q-fab-action
        :onclick="() => handleClick('corpus')"
        color="amber"
        text-color="black"
        icon="local_library"
        push
      >
        <ToolTip anchor="top middle" self="top middle" :offset="[0, 35]"> Create Corpus </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('collection')"
        color="amber"
        text-color="black"
        icon="apps"
        push
      >
        <ToolTip anchor="top middle" self="top middle" :offset="[0, 35]">
          Create Collection
        </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('dataset')"
        color="amber"
        text-color="black"
        icon="schema"
        push
      >
        <ToolTip anchor="top middle" self="top middle" :offset="[0, 35]"> Create Dataset </ToolTip>
      </q-fab-action>

      <q-fab-action
        :onclick="() => handleClick('workset')"
        color="amber"
        text-color="black"
        icon="work"
        push
      >
        <ToolTip anchor="top middle" self="top middle" :offset="[0, 35]"> Create Workset </ToolTip>
      </q-fab-action>
    </q-fab>

    <q-fab-action
      :onclick="() => handleClick('task')"
      color="amber"
      text-color="black"
      icon="assignment"
      push
    >
      <ToolTip anchor="center left" self="center right" :offset="[10, 10]"> Create Task </ToolTip>
    </q-fab-action>

    <q-fab-action
      :onclick="() => handleClick('ticket')"
      color="amber"
      text-color="black"
      icon="task"
      push
    >
      <ToolTip anchor="center left" self="center right" :offset="[10, 10]"> Create Ticket </ToolTip>
    </q-fab-action>
  </q-fab>
</template>

<script>
import { createId as cuid } from "@paralleldrive/cuid2";
import { defineComponent, ref } from "vue";
import { useEditing } from "@/use";
import { ToolTip } from "@/components";

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
