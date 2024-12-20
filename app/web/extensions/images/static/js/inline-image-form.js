class InlineImageBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
  render(placeholder, prefix, initialState, initialError) {
      const block = super.render(placeholder, prefix, initialState, initialError);
      const image = document.getElementById(`${prefix}-image`);
      const renderCaption = document.getElementById(`${prefix}-show_caption`);
      const captionFromFile = document.getElementById(`${prefix}-use_file_caption`);
      const captionText = document.getElementById(`${prefix}-caption`).closest("div.w-field__wrapper");
      const alignment = document.getElementById(`${prefix}-alignment`);

      const captionFileText = document.createElement("div");
      captionFileText.id = `${prefix}-file_text`;
      captionFileText.classList.add("caption-from-file");
      captionFileText.innerText = "No image selected.";
      captionText.parentElement.closest("div.w-field__wrapper").appendChild(captionFileText);

      const switchRenderCaption = () => {
        if (!renderCaption.checked) {
          captionFromFile.closest("div.w-panel__wrapper").classList.add("u-hide");
          document.getElementById(`${prefix}-caption-form-section`).classList.add("u-none");
        } else {
          captionFromFile.closest("div.w-panel__wrapper").classList.remove("u-hide");
          document.getElementById(`${prefix}-caption-form-section`).classList.remove("u-none");
        }
      }

      const switchCaptionFromFile = () => {
        if (!captionFromFile.checked) {
          captionFileText.classList.add("u-none");
          captionText.classList.remove("u-none");
        } else {
          captionFileText.classList.remove("u-none");
          captionText.classList.add("u-none");
        }
      }

      const switchParameters = () => {
        if (alignment.value == "main") {
          document.getElementById(`${prefix}-resize_rule`).closest("div.w-panel__wrapper").classList.add("u-hide");
          document.getElementById(`${prefix}-dimensions`).closest("div.w-panel__wrapper").classList.add("u-none");
          document.getElementById(`${prefix}-parameters`).closest("div.w-panel__wrapper").classList.add("u-none");
        } else {
          document.getElementById(`${prefix}-resize_rule`).closest("div.w-panel__wrapper").classList.remove("u-hide");
          document.getElementById(`${prefix}-dimensions`).closest("div.w-panel__wrapper").classList.remove("u-none");
          document.getElementById(`${prefix}-parameters`).closest("div.w-panel__wrapper").classList.remove("u-none");
        }
      }

      const setFileCaptionText = () => {
        if (image.value) {
          fetch(`/api/web/images/${image.value}/`)
          .then(response => response.json())
          .then(data => captionFileText.innerText = data.caption ? data.caption : "No caption is associated with the original image.");
        } else {
          captionFileText.innerText = "No image selected.";
        }
      }

      alignment.addEventListener("change", switchParameters);
      renderCaption.addEventListener("change", switchRenderCaption);
      captionFromFile.addEventListener("change", switchCaptionFromFile);
      image.addEventListener("change", setFileCaptionText);

      // set initial state
      setFileCaptionText();
      switchCaptionFromFile();
      switchRenderCaption();
      switchParameters();

      return block;
  }
}

window.telepath.register('webimage.InlineImageBlock', InlineImageBlockDefinition);
