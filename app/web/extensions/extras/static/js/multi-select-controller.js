/* eslint-disable no-undef */
class MultiSelectController extends window.StimulusModule.Controller {
  connect() {
    const selectEl = $(this.element);
    const selectMultiple = typeof selectEl.data("multiple") !== "undefined";
    const isSortable = typeof selectEl.data("sortable") !== "undefined";
    const placeholder = selectEl.data("placeholder");
    const useAPI = typeof selectEl.data("use-api") !== "undefined";
    const state = useAPI ? window.CustomUtils[selectEl.data("state-name")] : false;

    const selOptions = {
      width: "100%",
      dropdownAutoWidth: true,
      allowClear: true,
      placeholder: placeholder,
    };

    if (state && state.store.isMultiple) {
      state.store.isMultiple = selectMultiple;
    }

    if (state && state.store.templateSelection) {
      selOptions.templateSelection = state.store.templateSelection;
    }

    if (state && state.store.templateResult) {
      selOptions.templateResult = state.store.templateResult;
    }

    if (useAPI) {
      state.store.placeholder = selectEl.data("placeholder");
      selOptions.escapeMarkup = (option) => option;
      // define a custom data adapter for select2
      // https://select2.org/advanced/adapters-and-decorators
      $.fn.select2.amd.define(
        "select2/data/CustomAdapter",
        ["select2/data/array", "select2/utils"],
        function (ArrayData, Utils) {
          function CustomAdapter ($element, options) {
            CustomAdapter.__super__.constructor.call(this, $element, options);
          }

          Utils.Extend(CustomAdapter, ArrayData);

          CustomAdapter.prototype.item = function ($option) {
            const data = CustomAdapter.__super__.item.call(this, $option);
            const opt = $option[0];
            if (opt.tagName.toLowerCase() === "option") {
              for (const attrName of opt.getAttributeNames()) {
                if (!["value", "data-select2-id"].includes(attrName)) {
                  data[attrName] = opt.getAttribute(attrName);
                }
              }
            }
            return data;
          };
          CustomAdapter.prototype.query = state.queryAPI;

          return CustomAdapter;
        }
      );
      selOptions.dataAdapter = $.fn.select2.amd.require("select2/data/CustomAdapter");
    }

    selectEl.select2(selOptions);

    if (isSortable) {
      // we need to move the searchbox element inside of the selection container
      // so that it can show alongside the selected elements
      const container = selectEl.parent().find("ul.select2-selection__rendered");
      const searchBox = selectEl.parent().find("span.select2-search--inline").detach();
      searchBox.clone(true).appendTo(container);
      // now we make the container sortable
      container.sortable({
        containment: "parent",
        update: () => {
          container.children("li[title]").each((_i, obj) => {
            const el = selectEl.children(`option[username=${obj.title}]`);
            el.detach();
            selectEl.append(el);
          });
        },
      });
      // we also need to handle adding a new selection to prevent automatic sorting
      selectEl.on("select2:select", (e) => {
        const sel = selectEl.children(`option[value=${e.params.data.id}]`);
        sel.detach();
        selectEl.append(sel);
        selectEl.trigger("change");
      });
      // lastly select2 nukes the searchbox everytime it updates the selection container
      // so we need to restore it
      selectEl.on("change", () => {
        // the searchbox is removed AFTER triggering "change"
        // hence this horrible hack
        setTimeout(() => {
          if (container.find("span.select2-search--inline").length == 0) {
            searchBox.clone(true).appendTo(container);
          }
        }, 1);
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
