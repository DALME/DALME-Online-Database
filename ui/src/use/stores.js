import { storeToRefs } from "pinia";
import { EventBus } from "quasar";
import { inject, provide } from "vue";

import { useAuthStore } from "@/stores/auth";
import { useEditorStore } from "@/stores/editor";
import { useRecordStore } from "@/stores/records";
import { useSettingsStore } from "@/stores/settings";
import { useTaskStore } from "@/stores/tasks";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const views = useViewStore();
  const settings = useSettingsStore();
  const editorStore = useEditorStore();
  const taskStore = useTaskStore();
  const recordStore = useRecordStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    views,
    settings,
    editorStore,
    taskStore,
    recordStore,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(settings),
    ...storeToRefs(editorStore),
    ...storeToRefs(taskStore),
  });
  return {
    eventBus,
    auth,
    ui,
    views,
    settings,
    editorStore,
    taskStore,
    recordStore,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(settings),
    ...storeToRefs(editorStore),
    ...storeToRefs(taskStore),
  };
};

export const useStores = () => inject(StoresSymbol);
