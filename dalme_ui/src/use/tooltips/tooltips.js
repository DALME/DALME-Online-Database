import { inject, provide, computed } from "vue";
import { usePrefStore } from "@/stores/preferences";

const TooltipsSymbol = Symbol();

export const provideTooltips = () => {
  const prefStore = usePrefStore();
  const showTips = computed({
    get() {
      return prefStore.ui.tooltipsOn;
    },
    set(newValue) {
      prefStore.ui.tooltipsOn = newValue;
    },
  });

  provide(TooltipsSymbol, { showTips });
};

export const useTooltips = () => inject(TooltipsSymbol);
