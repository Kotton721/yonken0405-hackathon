
export const toggleState = (prevState, id) => ({
  ...prevState,
  [id]: !prevState[id],
});
