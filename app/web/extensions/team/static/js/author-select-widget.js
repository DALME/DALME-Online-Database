window.CustomUtils.userSelectState.connectCallback = (selectEl) => {
  const store = window.CustomUtils.userSelectState.store;
  store.selectEl = selectEl;
  store.byline = document.getElementById("id_byline_text");
  store.updateByline = () => {
    const data = store.selectEl.select2("data");
    if (data.length) {
      const name_list = store.selectEl.select2("data").map((x) => x.name);
      if (name_list.length === 1) {
        store.byline.value = name_list[0];
      } else if (name_list.length === 2) {
        store.byline.value = name_list.join(" and ");
      } else {
        const last = name_list.pop();
        store.byline.value = name_list.join(", ") + ", and " + last;
      }
    }
  };
  selectEl.on("change", store.updateByline);
};
