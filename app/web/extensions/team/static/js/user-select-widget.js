/* eslint-disable max-len */
window.CustomUtils.userSelectState = {
  store: {
    baseApiUrl: "/api/web/user/",
    placeholder: "",
    isMultiple: false,
    handleFormFields: false,
    avatarUrl: "",
    avatarPreview: null,
    avatarButton: null,
    selectEl: null,
    nameField: null,
    iconPlaceholder: "<svg class=\"icon icon-user user-placeholder\" aria-hidden=\"true\"><use href=\"#icon-user\"></use></svg>",
    getAvatarHTML: (url) => {
      const tenant = window.CustomUtils.constants.tenant;
      url = url.startsWith("/media") || url.startsWith("blob") ? url : `/media/${tenant}/${url}`;
      return `<div class="avatar-bg" style="background: center/cover url(${url});"></div>`;
    },
    templateSelection: (item) => {
      const store = window.CustomUtils.userSelectState.store;
      let avatar;
      if (store.handleFormFields) {
        store.avatarUrl = item.avatar;
        avatar = store.avatarUrl ? store.getAvatarHTML(store.avatarUrl) : store.iconPlaceholder;
      } else {
        avatar = item.avatar ? store.getAvatarHTML(item.avatar) : store.iconPlaceholder;
      }
      return `<div class="user-option">${avatar}<div class="user-label"><span>${item.name}</span>\
              <span class="user-username">${item.username||"no user account"}</span></div></div>`;
    },
    templateResult: (item) => {
      const store = window.CustomUtils.userSelectState.store;
      return store.templateSelection(item);
    },
    toggleForm: () => {
      const store = window.CustomUtils.userSelectState.store;
      const value = store.selectEl.select2("data")[0];
      store.nameField.value = value ? value.name : "";
      store.avatarPreview.innerHTML = store.avatarUrl ? store.getAvatarHTML(store.avatarUrl) : store.iconPlaceholder;
      store.avatarButton.innerHTML = store.avatarUrl ? "Remove avatar" : "Upload avatar";
    },
    avatarAction: (e) => {
      const store = window.CustomUtils.userSelectState.store;
      const action = e.target.innerHTML;
      const checkbox = document.getElementById("avatar-clear_id");
      const input = document.getElementById("id_avatar");
      if (action === "Upload avatar") {
        input.addEventListener("change", (e) => {
          if (e.target.files[0]) {
            store.avatarUrl = URL.createObjectURL(e.target.files[0]);
            checkbox.checked = false;
            store.toggleForm();
          };
        });
        input.click();
      } else {
        store.avatarUrl = "";
        checkbox.checked = true;
        store.toggleForm();
      }
    }
  },
  queryAPI: (params, callback) => {
    const store = window.CustomUtils.userSelectState.store;
    const url = params.term ? `${store.baseApiUrl}?name=${params.term}` : store.baseApiUrl;
    fetch(url)
    .then(response => response.json())
    .then(data => callback({
        results: data,
        more: false,
        context: null,
      })
    );
  },
  connectCallback: (selectEl) => {
    const store = window.CustomUtils.userSelectState.store;
    store.handleFormFields = typeof selectEl.data("handle-form-fields") !== "undefined";
    if (store.handleFormFields) {
      store.selectEl = selectEl;
      store.avatarPreview = document.getElementById("avatar-image-container");
      store.avatarButton = document.getElementById("avatar-file-input-button");
      store.nameField = document.getElementById("id_name");
      selectEl.on("change", store.toggleForm);
      store.avatarButton.addEventListener("click", store.avatarAction);
    }
  },
  disconnectCallback: (_selectEl) => {
    delete window.CustomUtils.userSelectState;
  },
};
