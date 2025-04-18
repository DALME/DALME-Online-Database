import { inject, provide } from "vue";

import { API } from "@/api";

const APISymbol = Symbol();

export const provideAPI = () => {
  provide(APISymbol, { apiInterface: () => API() });
};

export const useAPI = () => inject(APISymbol);
