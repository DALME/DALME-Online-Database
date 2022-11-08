import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useNavStore } from "@/stores/navigation";
import { usePrefStore } from "@/stores/preferences";
import { useUiStore } from "@/stores/ui";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const nav = useNavStore();
  const prefs = usePrefStore();
  const ui = useUiStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    nav,
    prefs,
    ui,
    ...storeToRefs(auth),
    ...storeToRefs(nav),
    ...storeToRefs(prefs),
    ...storeToRefs(ui),
  });
  return {
    eventBus,
    auth,
    nav,
    prefs,
    ui,
    ...storeToRefs(auth),
    ...storeToRefs(nav),
    ...storeToRefs(prefs),
    ...storeToRefs(ui),
  };
};

export const useStores = () => inject(StoresSymbol);
