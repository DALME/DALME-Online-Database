class ReferenceSource extends window.React.Component {
  constructor(props) {
      super(props);
      this.onChosen = this.onChosen.bind(this);
      this.onClose = this.onClose.bind(this);
  }

  componentDidMount() {
      const { onClose, entity } = this.props;
      const url = this.props.entityType?.chooserUrls["referenceChooser"];
      const urlParams = {};
      let entityId = null;

      if (entity) {
        entityId = entity.getData().id;
        urlParams.id = entityId;
        urlParams.biblio = entity.getData().biblio;
        urlParams.reference = entity.getData().reference;
        urlParams.mode = "edit";
      }

      $(document.body).on("hidden.bs.modal", this.onClose);

      const processAPIResults = (data) => {
        return {results: data.map((entry) => {
          const citation = new window.cite(entry);
          return {
            id: entry.id.split("/")[1],
            text: citation.format("citation", { format: "text", template: "apa", lang: "en-US" }),
            html: $(citation.format("bibliography", { format: "html", template: "apa", lang: "en-US" })),
          };
        })};
      }

      const getInitialValue = (el, callback) => {
        fetch(`${window.APIURL}/library/${entityId}/?content=csljson&format=json`)
        .then(response => response.json())
        .then(data => {
          const citation = new window.cite(data[0]);
          const text = citation.format("citation", { format: "text", template: "apa", lang: "en-US" });
          callback({id: entityId, text:text});
        });
      }

      const onload = {
        enter_reference: function(modal, jsonData) {
            const selectEl = $("#id_reference-id");
            selectEl.select2({
              placeholder: "Select reference or type to search...",
              width: "100%",
              dropdownParent: $(".modal"),
              containerCssClass: "select-reference",
              ajax: {
                url: `${window.APIURL}/library/`,
                dataType: "json",
                quietMillis: 500,
                results: processAPIResults,
                data: (term, page) => ({
                  search: term,
                  limit: 10,
                  content: "csljson",
                  format: "json"
                }),
              },
              initSelection: getInitialValue,
              formatResult: (entry) => entry.html,
              formatSelection: (entry) => entry.text,
            });

            $("form", modal.body).on("submit", function(evt) {
                $("#id_reference-reference").val(selectEl.select2("data").text);
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
