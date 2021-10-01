import { inject, provide } from "vue";

const TransportSymbol = Symbol();

export const provideTransport = (tracked) => provide(TransportSymbol, tracked);

export const useTransport = () => inject(TransportSymbol);
