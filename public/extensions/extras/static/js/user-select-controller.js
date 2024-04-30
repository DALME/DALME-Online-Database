class UserSelectController extends window.StimulusModule.Controller {
  static uploadUrl = "";
  static avatarUrl = "";
  static selectedUserData = "";

  connect() {
      const selectEl = $("[data-user-select]");
      const handleFormFields = typeof selectEl.data("handle-form-fields") !== "undefined";

      selectEl.select2({
        placeholder: $('<div class="user-option"><div class="text-placeholder">Select user...</div></div>'),
        allowClear: true,
        dropdownAutoWidth: true,
        width: "100%",
        templateResult: (item) => $(item.text),
        templateSelection: (item) => $(item.text),
      });

      if (handleFormFields) {
        const optData = selectEl.data("options");
        const fileField = $("#id_photo");
        const userIcon = '<svg class="icon icon-user user-placeholder" aria-hidden="true"><use href="#icon-user"></use></svg>';
        fileField.parent().parent().append(`<div id="user-form-avatar-preview">${userIcon}</div>`);

        const previewAvatar = document.getElementById("user-form-avatar-preview")
        const nameField = document.getElementById("id_name");

        const previewUrl = () => this.uploadUrl || this.avatarUrl;

        const togglePreview = () => {
          const url = previewUrl();
          if (url) {
            previewAvatar.innerHTML = "";
            previewAvatar.style.background = `center / cover url(${url})`;
          } else {
            previewAvatar.innerHTML = userIcon;
            previewAvatar.style.background = "none";
          }
        }

        const toggleForm = () => {
          if (this.selectedUserData) {
            nameField.value = this.selectedUserData.name;
            this.avatarUrl = this.selectedUserData.avatar ? this.selectedUserData.avatar : "";
          } else {
            nameField.value = "";
            this.avatarUrl = "";
          }
          togglePreview();
        }

        fileField.on("change", () => {
          const [file] = fileField.prop("files");
          this.uploadUrl = file ? URL.createObjectURL(file) : null;
          togglePreview();
        });

        selectEl.on("change", () => {
          const selID = selectEl.val();
          this.selectedUserData = selID ? optData[selID] : "";
          toggleForm();
        });
      }
  }
}

window.wagtail.app.register('userselect', UserSelectController);
