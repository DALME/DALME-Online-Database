class MultiSelectController extends window.StimulusModule.Controller {
  connect() {
    const selectEl = $(this.element);
    const selectMultiple = typeof selectEl.data("multiple") !== "undefined";
    const isSortable = typeof selectEl.data("sortable") !== "undefined";
    const state = selectEl.data("use-state") ? window.CustomUtils[selectEl.data("use-state")] : false;

    const selOptions = {
      width: "100%",
      dropdownAutoWidth: true,
      allowClear: true,
      containerCssClass: selectEl.data("container-classes"),
    }

    if (state) {
      state.store.placeholder = selectEl.data("placeholder");
      if (!state.store.useAPI) {
        state.store.dataMatcher = selectEl.data("options").data;
        state.store.optionsList = selectEl.data("options").options;
      }
      if (state.store.formatOptions) {
        selOptions.formatResult = state["resultFormatter"];
        selOptions.formatSelection = state["selectionFormatter"];
        selOptions.escapeMarkup = (option) => option;
        if (isSortable && !state.store.useAPI) selOptions.data = state.store.optionsList;
      }
    }

    if (selectMultiple && isSortable && !state.store.useAPI) {
      selOptions.multiple = true;
      selOptions.initSelection = (el, callback) => {
        const data = [];
        JSON.parse(el.val().replaceAll(`'`, `"`)).forEach((id) => {
            data.push({id: id, text: state["initialFormatter"](id)});
        });
        selectEl.val('');
        callback(data);
      };
    }

    if (state.store.useAPI) {
      selOptions.initSelection = state["initialFormatter"];
    }

    selectEl.select2(selOptions);

    if (selectMultiple) {
      if (isSortable) {
        selectEl.select2("container").find("ul.select2-choices").sortable({
          containment: "parent",
          start: () => selectEl.select2("onSortStart"),
          update: () => selectEl.select2("onSortEnd"),
        });
      }
    }

    if (state && state.connectCallback) state.connectCallback(selectEl);
  }

  disconnect() {
    const selectEl = $(this.element);
    const state = selectEl.data("use-state") ? window.CustomUtils[selectEl.data("use-state")] : false;
    if (state && state.disconnectCallback) state.disconnectCallback(selectEl);
    selectEl.select2("destroy");
  }
}

window.wagtail.app.register('multiselect', MultiSelectController);
