window.CustomUtils.userSelectState = {
  store: {
    baseApiUrl: "/api/public/user/",
    placeholder: "",
    handleFormFields: false,
    avatarUrl: "",
    iconPlaceholder: '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>',
    getAvatarHTML: (url) => `<div class="avatar-bg" style="background: center/cover url(${url});"></div>`,
    getFormattedItem: (item) => {
      const store = window.CustomUtils.userSelectState.store;
      const avatar = item.avatar ? store.getAvatarHTML(item.avatar) : store.iconPlaceholder;
      return `<div class="user-option">${avatar}<div class="user-label">${item.name} <span>${item.username}</span></div></div>`;
    },
    getIdList: (val) => JSON.parse(val.replaceAll(`'`, `"`)),
    fetchResults: (url, callback) => {
      const results = [];
      const store = window.CustomUtils.userSelectState.store;
      fetch(url)
      .then(response => response.json())
      .then(data => {
          data.forEach((item) => {
            results.push({
              id: item.id,
              text: store.getFormattedItem(item),
              item: item,
            });
          });
          callback(results);
      });
    },
  },
  queryAPI: (options) => {
    const store = window.CustomUtils.userSelectState.store;
    const url = options.term ? `${store.baseApiUrl}?name=${options.term}` : store.baseApiUrl;
    store.fetchResults(url, (results) => {
      options.callback({
        results: results,
        more: false,
        context: null,
      });
    });
  },
  initialFormatter: (el, callback) => {
    const store = window.CustomUtils.userSelectState.store;
    const id_list = store.getIdList(el.val());
    store.fetchResults(`${store.baseApiUrl}?id__in=${id_list}`, (results) => {
      el.val('');
      callback(results);
    });
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
        const value = selectEl.select2("data");
        if (value) {
          nameField.value = value.item.name;
          store.avatarUrl = value.item.avatar ? value.item.avatar : "";
        } else {
          nameField.value = "";
          store.avatarUrl = "";
        }
        togglePreview();
      }

      selectEl.on("change", toggleForm);
    }
  },
  disconnectCallback: (selectEl) => {
    delete window.CustomUtils.userSelectState;
  },
}
