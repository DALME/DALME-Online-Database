
class GradientChooserModal {
  onloadHandlers = window.CHOOSER_MODAL_ONLOAD_HANDLERS;
  chosenResponseName = 'chosen'; // identifier for the ModalWorkflow response that indicates an item was chosen

  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  getURL(opts) {
    return this.baseUrl;
  }

  getURLParams(opts) {
    const urlParams = {};
    if (opts.multiple) {
      urlParams.multiple = 1;
    }
    if (opts.linkedFieldFilters) {
      Object.assign(urlParams, opts.linkedFieldFilters);
    }
    return urlParams;
  }

  open(opts, callback) {
    // eslint-disable-next-line no-undef
    ModalWorkflow({
      url: this.getURL(opts || {}),
      urlParams: this.getURLParams(opts || {}),
      onload: this.onloadHandlers,
      responses: {
        [this.chosenResponseName]: (result) => {
          callback(result);
        },
      },
    });
  }
}

class GradientChooser extends window.Chooser {
  chooserModalClass = GradientChooserModal;

  initHTMLElements(id) {
    super.initHTMLElements(id);
    this.previewGradient = this.chooserElement.querySelector('[data-chooser-gradient]');
  }

  getStateFromHTML() {
    const state = super.getStateFromHTML();
    if (state) {
      state.gradient = this.previewGradient.innerHTML;
      state.description = this.titleElement.textContent;
    }
    return state;
  }

  renderState(newState) {
    this.input.setAttribute('value', newState.id);
    this.input.dispatchEvent(new Event('change', { bubbles: true }));
    this.titleElement.textContent = newState.description;
    this.previewGradient.innerHTML = newState.gradient;
    this.chooserElement.classList.remove('blank');
    if (this.editLink) {
      const editUrl = newState[this.editUrlStateKey];
      if (editUrl) {
        this.editLink.setAttribute('href', editUrl);
        this.editLink.hidden = false;
      } else {
        this.editLink.hidden = true;
      }
    }
  }

}

ChooserFactory = window.telepath.unpack("wagtail.admin.widgets.Chooser").constructor

class GradientChooserFactory extends ChooserFactory {
  widgetClass = GradientChooser;
  chooserModalClass = GradientChooserModal;
}

window.GradientChooser = GradientChooser;
window.GradientChooserFactory = GradientChooserFactory;
window.GradientChooserModal = GradientChooserModal;
