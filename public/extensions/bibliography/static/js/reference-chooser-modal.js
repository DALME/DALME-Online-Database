
class ReferenceSource extends window.React.Component {

  constructor(props) {
      super(props);
      this.onChosen = this.onChosen.bind(this);
      this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
      const { onClose, editorState, entity, entityType } = this.props;
      const url = window.chooserUrls.referenceChooser;
      $(document.body).on("hidden.bs.modal", this.onClose);
      const urlParams = {}
      let entityId = null;

      if (entity) {
        entityId = entity.getData().id;
        urlParams.id = entityId;
        urlParams.biblio = entity.getData().biblio;
        urlParams.reference = entity.getData().reference;
        urlParams.mode = "edit";
      }

      const onload = {
        enter_reference: function(modal, jsonData) {
            const selector = window.reference_dialogue("#id_reference-id", entityId);

            $("form", modal.body).on("submit", function() {
                const sdata = selector.select2("data");
                $("#id_reference-reference").val(sdata[0].text);
                modal.postForm(this.action, $(this).serialize());
                return false;
            });
        },

        reference_chosen: function(modal, jsonData) {
            modal.respond("referenceEntered", jsonData["result"]);
            modal.close();
        }
      };

      this.workflow = window.ModalWorkflow({
        url,
        urlParams,
        onload,
        responses: {
          referenceEntered: (data) => this.onChosen(data),
        },
        onError: () => {
          window.alert("There was an error.");
          onClose();
        },
      });
  }

  componentWillUnmount() {
    this.workflow = null;
    $(document.body).off("hidden.bs.modal", this.onClose);
  }

  onChosen(data) {
    const { editorState, entity, entityKey, entityType, onComplete } = this.props;
    const content = editorState.getCurrentContent();
    const selection = editorState.getSelection();

    let nextState;
    const contentWithEntity = content.createEntity(entityType.type, "IMMUTABLE", data);
    const newEntityKey = contentWithEntity.getLastCreatedEntityKey();
    nextState = window.DraftJS.RichUtils.toggleLink(editorState, selection, newEntityKey);

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

class ReferenceDecorator extends window.draftail.TooltipEntity {

  render() {
    const { entityKey, contentState, children } = this.props;
    const data = contentState.getEntity(entityKey).getData();
    const { showTooltipAt } = this.state;

    const summary = window.React.createElement("div", {
      id: entityKey,
      className: "TooltipText",
    }, data.reference );

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

    return window.React.createElement("a", {
      role: "button",
      onMouseUp: this.openTooltip,
      className: `TooltipEntity id_${data.id}`,
      title: data.text,
      "data-draftail-trigger": true,
    }, [
        window.React.createElement(window.wagtail.components.Icon, {
          name: "bookmark",
          className: "tooltip-entity-reference-icon",
        }),
        children,
        (showTooltipAt && window.React.createElement(window.wagtail.components.Portal, {
          node: showTooltipAt.container,
          onClose: this.closeTooltip,
          closeOnClick: true,
          closeOnType: true,
          closeOnResize: true,
        }, tooltip))
      ]);
  }
}


// Register the plugin directly on script execution so the editor loads it when initialising.
window.draftail.registerPlugin({
  type: 'REFERENCE',
  source: ReferenceSource,
  decorator: ReferenceDecorator,
});
