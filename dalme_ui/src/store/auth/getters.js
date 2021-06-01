import { isNil } from "ramda";

export const isAuthenticated = (state) => !isNil(state.user.id);
export const userId = (state) => state.user.id;
