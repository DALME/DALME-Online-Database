class FootnoteSource extends window.React.Component {

    constructor(props) {
        super(props);
        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
        const { onClose, entity } = this.props;
        const url = this.props.entityType?.chooserUrls["footnoteEntry"];
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
          onClose();
        }

        // add dialogue to body and hide it, so content can be added to it before display
        $("body").append(dialogue);
        dialogue.hide();
        dialogue.on("click", ".footnote-modal-cancel", closeDialogue)

        const onload = {
          enter_footnote: function(modal, jsonData) {
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
      const { editorState, entity, entityType, entityKey, onComplete } = this.props;
      const contentState = editorState.getCurrentContent();
      let selectionState = editorState.getSelection();
      let nextState = null;

      if (!entity) { // if entity needs to be created
          // collapse selection if necessary
          if (selectionState.getStartOffset() != selectionState.getEndOffset()) {
            selectionState = selectionState.merge({ anchorOffset: selectionState.focusOffset });
          }
          // determine if we're at the very end of the block
          const block = contentState.getBlockForKey(selectionState.getStartKey());
          const atEnd = block.getLength() == selectionState.anchorOffset;
          // create entity
          const contentWithEntity = contentState.createEntity(entityType.type, "IMMUTABLE", data);
          // add the call-out
          let contentWithCallout = window.DraftJS.Modifier.insertText(
            contentState,
            selectionState,
            "✱",
            null,
            contentWithEntity.getLastCreatedEntityKey()
          );
          // set selection after call-out
          const selectionStateAfterCallout = selectionState.merge({
            anchorOffset: selectionState.anchorOffset + 1,
            focusOffset: selectionState.focusOffset + 1,
          });
          // add space after if at end
          if (atEnd) {
            contentWithCallout = window.DraftJS.Modifier.insertText(
              contentWithCallout, selectionStateAfterCallout, " ", null, null
            );
          }
          // create new editorState object
          const newEditorState = window.DraftJS.EditorState.set(
            editorState, { currentContent: contentWithCallout }
          );
          // move selection after call-out
          nextState = window.DraftJS.EditorState.forceSelection(newEditorState, selectionStateAfterCallout);

      } else { // if entity already exists
        const contentMerged = contentState.mergeEntityData(entityKey, data);
        nextState = window.DraftJS.EditorState.push(editorState, contentMerged, "merge-entity-data");
      }
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
