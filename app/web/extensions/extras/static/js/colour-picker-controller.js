class ColorController extends window.StimulusModule.Controller {
  static values = { swatches: Array, theme: String };

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

window.wagtail.app.register('color', ColorController);
