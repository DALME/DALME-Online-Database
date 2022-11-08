import { inject, provide, computed } from "vue";
import { usePrefStore } from "@/stores/preferences";

const TooltipsSymbol = Symbol();

export const provideTooltips = () => {
  const prefStore = usePrefStore();
  const showTips = computed({
    get() {
      return prefStore.general.tooltipsOn;
    },
    set(newValue) {
      prefStore.general.tooltipsOn = newValue;
    },
  });

  provide(TooltipsSymbol, { showTips });
};

export const useTooltips = () => inject(TooltipsSymbol);
