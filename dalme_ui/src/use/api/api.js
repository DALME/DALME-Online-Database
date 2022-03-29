import { inject, provide } from "vue";

import { API } from "@/api";

const APISymbol = Symbol();

export const provideAPI = (reauthenticate) => {
  provide(APISymbol, { apiInterface: () => API(reauthenticate) });
};

export const useAPI = () => inject(APISymbol);
