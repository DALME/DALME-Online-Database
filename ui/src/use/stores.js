import { storeToRefs } from "pinia";
import { EventBus } from "quasar";
import { inject, provide } from "vue";

import { useAuthStore } from "@/stores/auth";
import { useEditorStore } from "@/stores/editor";
import { useUiStore } from "@/stores/ui";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const editorStore = useEditorStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    editorStore,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(editorStore),
  });
  return {
    eventBus,
    auth,
    ui,
    editorStore,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(editorStore),
  };
};

export const useStores = () => inject(StoresSymbol);
