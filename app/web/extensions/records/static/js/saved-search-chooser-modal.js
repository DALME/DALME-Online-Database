/* eslint-disable no-undef */

class SavedSearchSource extends window.React.Component {

  constructor(props) {
      super(props);
      this.onChosen = this.onChosen.bind(this);
      this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
      const { onClose, entity } = this.props;
      const url = this.props.entityType?.chooserUrls["savedSearchChooser"];
      $(document.body).on("hidden.bs.modal", this.onClose);
      const urlParams = {};
      let entityId = null;

      if (entity) {
        entityId = entity.getData().id;
        urlParams.id = entityId;
        urlParams.mode = "edit";
      }

      const onload = {
        enter_saved_search: function(modal, _jsonData) {
            $("form", modal.body).on("submit", function() {
                const select = document.getElementById("id_saved_search-id");
                document.getElementById("id_saved_search-name").value =
                  select.options[select.selectedIndex].text;
                modal.postForm(this.action, $(this).serialize());
                return false;
            });
        },

        saved_search_chosen: function(modal, jsonData) {
            modal.respond("savedSearchEntered", jsonData["result"]);
            modal.close();
        }
      };

      this.workflow = window.ModalWorkflow({
        url,
        urlParams,
        onload,
        responses: {
          savedSearchEntered: (data) => this.onChosen(data),
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
    const { editorState, entityType, onComplete } = this.props;
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

class SavedSearchDecorator extends window.draftail.TooltipEntity {

  render() {
    const { entityKey, contentState, children } = this.props;
    const data = contentState.getEntity(entityKey).getData();
    const { showTooltipAt } = this.state;

    const summary = window.React.createElement("div", {
      id: entityKey,
      className: "TooltipText",
    }, data.name );

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
      title: data.name,
      "data-draftail-trigger": true,
    }, [
        window.React.createElement(window.wagtail.components.Icon, {
          name: "magnifying-glass-location",
          className: "tooltip-entity-saved-search-icon",
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
  type: "SAVED_SEARCH",
  source: SavedSearchSource,
  decorator: SavedSearchDecorator,
});
