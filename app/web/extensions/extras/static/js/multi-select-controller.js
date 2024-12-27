/* eslint-disable no-undef */
class MultiSelectController extends window.StimulusModule.Controller {
  connect() {
    const selectEl = $(this.element);
    const selectMultiple = typeof selectEl.data("multiple") !== "undefined";
    const isSortable = typeof selectEl.data("sortable") !== "undefined";
    const useAPI = typeof selectEl.data("use-api") !== "undefined";
    const state = useAPI ? window.CustomUtils[selectEl.data("state-name")] : false;

    const selOptions = {
      width: "100%",
      dropdownAutoWidth: true,
      allowClear: true,
      containerCssClass: selectEl.data("container-classes"),
    };

    if (selectMultiple && selectEl.prop("tagName") != "SELECT") {
      selOptions.multiple = true;
    }

    if (useAPI) {
      state.store.placeholder = selectEl.data("placeholder");
      selOptions.query = state["queryAPI"];
      selOptions.escapeMarkup = (option) => option;
    }

    if (isSortable || useAPI) {
      selOptions.initSelection = state["initialFormatter"];
    }

    selectEl.select2(selOptions);

    if (isSortable) {
      selectEl.select2("container").find("ul.select2-choices").sortable({
        containment: "parent",
        start: selectEl.select2("onSortStart"),
        update: selectEl.select2("onSortEnd"),
      });
    }

    if (state && state.connectCallback) state.connectCallback(selectEl);
  }

  disconnect() {
    const selectEl = $(this.element);
    const state = selectEl.data("use-state")
      ? window.CustomUtils[selectEl.data("use-state")]
      : false;
    if (state && state.disconnectCallback) state.disconnectCallback(selectEl);
    selectEl.select2("destroy");
  }
}

window.wagtail.app.register("multiselect", MultiSelectController);
