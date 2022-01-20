import { inject, provide } from "vue";
import { useStore } from "vuex";

const PermissionsSymbol = Symbol();

export const providePermissions = () => {
  const $store = useStore();

  const permissions = { isAdmin: $store.getters["auth/isAdmin"] };

  provide(PermissionsSymbol, { permissions });
};

export const usePermissions = () => inject(PermissionsSymbol);
