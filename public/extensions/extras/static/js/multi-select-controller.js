class MultiSelectController extends window.StimulusModule.Controller {
  connect() {
    const selectEl = $("[data-multiselect]");
    selectEl.select2({
      width: "100%",
      dropdownAutoWidth: true,
    });

    const fieldName = selectEl.attr("name");
    const form = selectEl.parents("form");
    form.on("formdata", (evt) => {
      evt.formData.set(fieldName, selectEl.val());
    });

  }
}

window.wagtail.app.register('multiselect', MultiSelectController);
