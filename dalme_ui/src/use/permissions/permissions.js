import { inject, provide } from "vue";
import { useAuthStore } from "@/stores/auth";

const PermissionsSymbol = Symbol();

export const providePermissions = () => {
  const $authStore = useAuthStore();
  const permissions = { isAdmin: $authStore.isAdmin };

  provide(PermissionsSymbol, { permissions });
  return permissions;
};

export const usePermissions = () => inject(PermissionsSymbol);
