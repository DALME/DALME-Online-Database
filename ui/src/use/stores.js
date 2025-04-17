import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
import { useSettingsStore } from "@/stores/settings";
import { useEditorStore } from "@/stores/editor";
import { useTaskStore } from "@/stores/tasks";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const views = useViewStore();
  const settings = useSettingsStore();
  const editorStore = useEditorStore();
  const taskStore = useTaskStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    views,
    settings,
    editorStore,
    taskStore,
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
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(settings),
    ...storeToRefs(editorStore),
    ...storeToRefs(taskStore),
  };
};

export const useStores = () => inject(StoresSymbol);
