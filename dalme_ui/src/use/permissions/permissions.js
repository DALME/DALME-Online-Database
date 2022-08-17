import { inject, provide } from "vue";
import { useAuthStore } from "@/stores/auth";

const PermissionsSymbol = Symbol();

export const providePermissions = () => {
  const $store = useAuthStore();

  const permissions = { isAdmin: $store.isAdmin };

  provide(PermissionsSymbol, { permissions });
  return permissions;
};

export const usePermissions = () => inject(PermissionsSymbol);
