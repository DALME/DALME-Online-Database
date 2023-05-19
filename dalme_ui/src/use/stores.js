import { EventBus } from "quasar";
import { inject, provide } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useNavStore } from "@/stores/navigation";
import { usePrefStore } from "@/stores/preferences";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";

const StoresSymbol = Symbol();

export const provideStores = () => {
  const eventBus = new EventBus();
  const auth = useAuthStore();
  const nav = useNavStore();
  const prefs = usePrefStore();
  const ui = useUiStore();
  const views = useViewStore();

  provide(StoresSymbol, {
    eventBus,
    auth,
    nav,
    prefs,
    ui,
    views,
    ...storeToRefs(auth),
    ...storeToRefs(nav),
    ...storeToRefs(prefs),
    ...storeToRefs(ui),
    ...storeToRefs(views),
  });
  return {
    eventBus,
    auth,
    nav,
    prefs,
    ui,
    views,
    ...storeToRefs(auth),
    ...storeToRefs(nav),
    ...storeToRefs(prefs),
    ...storeToRefs(ui),
    ...storeToRefs(views),
  };
};

export const useStores = () => inject(StoresSymbol);
