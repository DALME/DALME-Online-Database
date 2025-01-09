import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";
import { usePreferencesStore } from "@/stores/preferences";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const ui = useUiStore();
  const views = useViewStore();
  const preferences = usePreferencesStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    ui,
    views,
    preferences,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(preferences),
  });
  return {
    eventBus,
    auth,
    ui,
    views,
    preferences,
    ...storeToRefs(auth),
    ...storeToRefs(ui),
    ...storeToRefs(views),
    ...storeToRefs(preferences),
  };
};

export const useStores = () => inject(StoresSymbol);
