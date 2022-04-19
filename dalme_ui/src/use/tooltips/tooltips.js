import { inject, provide, ref } from "vue";

const TooltipsSymbol = Symbol();

export const provideTooltips = () => {
  const showTips = ref(true);

  provide(TooltipsSymbol, { showTips });
};

export const useTooltips = () => inject(TooltipsSymbol);
