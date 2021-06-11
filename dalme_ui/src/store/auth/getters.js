import { isNil } from "ramda";

export const isAdmin = (state) => state.user.isAdmin;
export const isAuthenticated = (state) => !isNil(state.user.id);
export const userId = (state) => state.user.id;
