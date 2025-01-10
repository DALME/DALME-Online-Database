import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
import { useSettingsStore } from "@/stores/settings";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const views = useViewStore();
  const settings = useSettingsStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    views,
    settings,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(settings),
  });
  return {
    eventBus,
    auth,
    ui,
    views,
    settings,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(settings),
  };
};

export const useStores = () => inject(StoresSymbol);
