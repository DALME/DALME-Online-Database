export const addUser = (state, data) => (state.user = data);

export const deleteUser = (state) =>
  (state.user = { id: null, username: null });
