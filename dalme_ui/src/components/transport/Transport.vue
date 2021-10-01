<template>
  <q-drawer
    side="right"
    v-model="show"
    show-if-above
    bordered
    :breakpoint="500"
    class="bg-grey-3"
  >
    <q-scroll-area class="fit">
      <div class="q-pa-sm">
        <ul>
          <li v-for="entry in history" :key="entry.timestamp">
            {{ entry }}
          </li>
        </ul>
        <p>
          <button @click="undo">Undo</button>
          <button @click="redo">Redo</button>
        </p>
      </div>
    </q-scroll-area>
  </q-drawer>
</template>

<script>
import { isEmpty } from "ramda";
import { computed, defineComponent, inject } from "vue";
import { useRefHistory } from "@vueuse/core";

export default defineComponent({
  name: "Transport",
  setup() {
    const tracked = inject("tracked");
    const { history, undo, redo } = useRefHistory(tracked, { deep: true });
    const show = computed({
      get: () => !isEmpty(history),
      set: () => !isEmpty(history),
    });

    return { history, undo, redo, show };
  },
});
</script>
