export const toggleState = (setState, id) => {
    setState((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };