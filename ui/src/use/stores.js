import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const views = useViewStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    views,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
  });
  return {
    eventBus,
    auth,
    ui,
    views,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
  };
};

export const useStores = () => inject(StoresSymbol);
