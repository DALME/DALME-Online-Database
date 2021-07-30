import { inject, provide } from "vue";

const PaginationSymbol = Symbol();

const pagination = () => null;

export const providePagination = () => provide(PaginationSymbol, pagination);

export const usePagination = () => inject(PaginationSymbol);
