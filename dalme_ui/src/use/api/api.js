import { API } from "@/api";
import { inject, provide } from "vue";

const APISymbol = Symbol();

export const provideAPI = (reauthenticate) =>
  provide(APISymbol, API(reauthenticate));

export const useAPI = () => inject(APISymbol);
