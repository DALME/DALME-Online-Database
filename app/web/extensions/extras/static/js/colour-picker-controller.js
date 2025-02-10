/* eslint-disable no-undef */
class ColorController extends window.StimulusModule.Controller {
  constructor() {
    super();
    this.swatchesValue = [];
    this.themeValue = "";
  }

  connect() {
      // create
      Coloris({ el: `#${this.element.id}` });

      // set options after initial creation
      setTimeout(() => {
          Coloris({
            swatches: this.swatchesValue,
            theme: this.themeValue,
            themeMode: getComputedStyle(document.body).getPropertyValue("color-scheme"),
          });
      });
  }
}

window.wagtail.app.register("color", ColorController);
