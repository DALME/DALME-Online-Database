class FootnoteSource extends window.React.Component {

    constructor(props) {
        super(props);
        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
        const { onClose, entity } = this.props;
        const url = window.chooserUrls.footnoteEntry;
        const urlParams = {};

        if (entity) {
          urlParams.pk = entity.getData().id;
        } else {
          urlParams.id = window.CustomUtils.getUUID();
        }

        const dialogue = $(
          '<div id="footnote-dialogue" tabindex="-1" role="dialog" aria-hidden="true">\
            <div class="modal-dialog"><div class="modal-content">\
                <button type="button" class="button close button--icon text-replace footnote-modal-cancel">\
                  <svg class="icon icon-cross" aria-hidden="true"><use href="#icon-cross"></use></svg>Close</button>\
              <div class="modal-body" data-w-dialog-target></div></div></div></div>'
        );
        const modalBg = $('<div class="modal-backdrop fade in"></div>');

        const openDialogue = () => {
          dialogue.show();
          $("body").append(modalBg);
          $(document.body).addClass("footnote-modal-body");
        }

        const closeDialogue = () => {
          dialogue.hide();
          dialogue.remove();
          modalBg.remove();
          $(document.body).removeClass("footnote-modal-body");
          document.querySelectorAll(".Draftail-Editor").forEach((el) => el.classList.remove("Draftail-Editor--readonly"));
          document.querySelectorAll(".public-DraftEditor-content").forEach((el) => el.contentEditable = true);
          this.onClose;
        }

        // add dialogue to body and hide it, so content can be added to it before display
        $("body").append(dialogue);
        dialogue.hide();
        dialogue.on("click", ".footnote-modal-cancel", closeDialogue)

        const onload = {
          enter_footnote: function(modal, jsonData) {
              // execute script that sets up note rich_text field
              // ModalWorkflow uses innerHTML to set the body, which doesn't eval the script
              eval(document.getElementById("id_footnote-text").nextElementSibling.innerHTML);

              openDialogue();

              $("form", modal.body).on("submit", function() {
                const action = entity ? `${this.action}${entity.getData().id}/` : this.action;
                modal.postForm(action, $(this).serialize());
                return false;
              });
          },
          footnote_entered: function(modal, jsonData) {
              modal.respond("footnoteEntered", jsonData["result"]);
              closeDialogue();
          }
        };

        this.workflow = window.ModalWorkflow({
          url,
          urlParams,
          onload,
          dialogId: "footnote-dialogue",
          responses: {
            footnoteEntered: (data) => this.onChosen(data),
          },
          onError: () => {
            window.alert("There was an error.");
            onClose();
          },
        });
    }

    componentWillUnmount() {
      this.workflow = null;
    }

    onChosen(data) {
      var { editorState, entity, entityType, entityKey, onComplete } = this.props;
      var content = editorState.getCurrentContent();
      var selection = editorState.getSelection();
      var finalContentState = {};
      var finalChangeType = "";

      if (selection.getStartOffset() != selection.getEndOffset()) {
        let newSelection = selection.merge({ anchorOffset: selection.focusOffset });
        selection = newSelection;
      }

      // if entity needs to be created
      if (!entity) {
          const contentWithEntity = content.createEntity(entityType.type, "IMMUTABLE", data);
          entityKey = contentWithEntity.getLastCreatedEntityKey();

          const contentWithCallout = window.DraftJS.Modifier.insertText(
            content,
            selection,
            "✱",
            null,
            entityKey
          );

          editorState = window.DraftJS.EditorState.push(editorState, contentWithCallout, "insert-characters");
          content = editorState.getCurrentContent();

          finalContentState = window.DraftJS.Modifier.applyEntity(content, selection, entityKey);
          finalChangeType = "apply-entity"
      } else {
        finalContentState = content.mergeEntityData(entityKey, data);
        finalChangeType = "merge-entity-data"
      }

      const nextState = window.DraftJS.EditorState.push(editorState, finalContentState, finalChangeType);
      this.workflow.close();
      onComplete(nextState);
    }

    onClose(e) {
      const { onClose } = this.props;
      e.preventDefault();
      onClose();
    }

    render() {
        return null;
    }
}

class FootnoteDecorator extends window.draftail.TooltipEntity {

    constructor(props) {
        super(props);
        this.onRemove = this.onRemove.bind(this);
    }

    onRemove(e) {
        e.preventDefault();
        e.stopPropagation();
        const { onRemove, entityKey, contentState } = this.props;
        const data = contentState.getEntity(entityKey).getData();
        const editor = document.querySelector(`.id_${data.id}`)
                        .closest("[data-streamfield-widget]")
                        .getElementsByTagName("input")[0]
                        .draftailEditor;
        onRemove(entityKey);
        setTimeout(() => {
          const editorState = editor.getEditorState();
          const content = editorState.getCurrentContent();
          const selection = editorState.getSelection();
          const newContentState = window.DraftJS.Modifier.removeRange(content, selection);
          const newEditorState = window.DraftJS.EditorState.push(editorState, newContentState, "remove-range");
          editor.onChange(newEditorState);
        }, 10);
    }

    render() {
      const { entityKey, contentState, children } = this.props;
      const data = contentState.getEntity(entityKey).getData();
      const { showTooltipAt } = this.state;
      const cleanText = window.CustomUtils.stripTags(data.text, "Footnote...");

      const summary = window.React.createElement("div", {
        id: entityKey,
        className: "footnoteTooltipText",
      }, cleanText);

      const editButton = window.React.createElement("button", {
        className: "button button-small Tooltip__button",
        onClick: this.onEdit,
      }, "Edit");

      const removeButton = window.React.createElement("button", {
        className: "button button-small button-secondary no Tooltip__button",
        onClick: this.onRemove,
      }, "Remove");

      const tooltip = window.React.createElement(window.draftail.Tooltip, {
        target: showTooltipAt,
        direction: "top",
      }, [summary, editButton, removeButton]);

      return (window.React.createElement("a", {
        role: "button",
        onMouseUp: this.openTooltip,
        className: `TooltipEntity id_${data.id}`,
        title: cleanText,
        "data-draftail-trigger": true,
      }, [
        window.React.createElement(window.wagtail.components.Icon, {
          name: "asterisk",
          className: "tooltip-entity-footnote-icon",
        }),
        (showTooltipAt && window.React.createElement(window.wagtail.components.Portal, {
          node: showTooltipAt.container,
          onClose: this.closeTooltip,
          closeOnClick: true,
          closeOnType: true,
          closeOnResize: true,
        }, tooltip))
      ]));
    }
}

window.draftail.registerPlugin({
    type: "FOOTNOTE",
    source: FootnoteSource,
    decorator: FootnoteDecorator,
});
