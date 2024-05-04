window.CustomUtils.userSelectState = {
  store: {
    placeholder: "",
    handleFormFields: false,
    formatOptions: true,
    useAPI: false,
    avatarUrl: "",
    selectedUserData: {},
    dataMatcher: {},
    optionsList: [],
    iconPlaceholder: '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>',
    getAvatarHTML: (url) => `<div class="avatar-bg" style="background: center/cover url(${url});"></div>`,
  },
  resultFormatter: (item) => {
    const store = window.CustomUtils.userSelectState.store;
    if (item.text == store.placeholder) {
      return `<div class="user-option"><div class="text-placeholder">${store.placeholder}</div></div>`;
    } else {
      return item.text;
    }
  },
  selectionFormatter: this.resultFormatter,
  initialFormatter: (id) => {
    const store = window.CustomUtils.userSelectState.store;
    const item = store.dataMatcher[id];
    const avatar = item.avatar ? store.getAvatarHTML(item.avatar) : store.iconPlaceholder;
    return `<div class="user-option">${avatar}<div class="user-label">${item.name} <span>${item.username}</span></div></div>`;
  },
  connectCallback: (selectEl) => {
    const store = window.CustomUtils.userSelectState.store;
    store.handleFormFields = typeof selectEl.data("handle-form-fields") !== "undefined";
    if (store.handleFormFields) {
      const photoChooser = document.getElementById("id_photo-chooser");
      const nameField = document.getElementById("id_name");

      const togglePreview = () => {
        photoChooser.querySelector(".chooser__image").src = store.avatarUrl ? store.avatarUrl : "#";
        if (!photoChooser.classList.contains("blank") || store.avatarUrl) {
          photoChooser.classList.toggle("blank");
        }
      }

      const toggleForm = () => {
        if (store.selectedUserData) {
          nameField.value = store.selectedUserData.name;
          store.avatarUrl = store.selectedUserData.avatar ? store.selectedUserData.avatar : "";
        } else {
          nameField.value = "";
          store.avatarUrl = "";
        }
        togglePreview();
      }

      selectEl.on("change", () => {
        const selID = selectEl.val();
        store.selectedUserData = selID ? store.dataMatcher[selID] : "";
        toggleForm();
      });
    }
  },
  disconnectCallback: (selectEl) => {
    delete window.CustomUtils.userSelectState;
  },
}
