const React = window.React;
const Modifier = window.DraftJS.Modifier;
const EditorState = window.DraftJS.EditorState;
const SelectionState = window.DraftJS.SelectionState;
const AtomicBlockUtils = window.DraftJS.AtomicBlockUtils;

const Uuid = function createUUID() {
   return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
   });
}

class FootnoteSource extends React.Component {

    constructor(props) {
        super(props);
        this.onChosen = this.onChosen.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    componentDidMount() {
        const { onClose, editorState, entity, entityType } = this.props;
        const url = global.chooserUrls.footnoteEntry;
        $(document.body).on('hidden.bs.modal', this.onClose);
        const urlParams = {}

        if (entity) {
          urlParams.note_id = entity.getData().note_id;
          urlParams.text = entity.getData().text;
          urlParams.mode = 'edit';
        } else {
          urlParams.note_id = Uuid();
          urlParams.text = null;
        }

        const onload = {
          enter_footnote: function(modal, jsonData) {
              $('p.link-types a', modal.body).on('click', function() {
                  modal.loadUrl(this.href);
                  return false;
              });

              $('form', modal.body).on('submit', function() {
                  modal.postForm(this.action, $(this).serialize());
                  return false;
              });
          },
          footnote_entered: function(modal, jsonData) {
              modal.respond('footnoteEntered', jsonData['result']);
              modal.close();
          }
        };

        this.workflow = global.ModalWorkflow({
          url,
          urlParams,
          onload,
          responses: {
            footnoteEntered: (data) => this.onChosen(data),
          },
          onError: () => {
            window.alert(STRINGS.SERVER_ERROR);
            onClose();
          },
        });
    }

    componentWillUnmount() {
      this.workflow = null;
      $(document.body).off('hidden.bs.modal', this.onClose);
    }

    onChosen(data) {
      var { editorState, entity, entityType, entityKey, onComplete } = this.props;
      var content = editorState.getCurrentContent();
      var selection = editorState.getSelection();
      var finalContentState = {};
      var finalChangeType = '';

      if (selection.getStartOffset() != selection.getEndOffset()) {
        let newSelection = selection.merge({ anchorOffset: selection.focusOffset });
        selection = newSelection;
      }

      // if entity needs to be created
      if (!entity) {
          const contentWithEntity = content.createEntity(entityType.type, 'IMMUTABLE', {
            note_id: data['note_id'],
            text: data['text']
          });
          entityKey = contentWithEntity.getLastCreatedEntityKey();

          const contentWithCallout = Modifier.insertText(
            content,
            selection,
            '✱',
            null,
            entityKey
          );

          editorState = EditorState.push(editorState, contentWithCallout, 'insert-characters');
          content = editorState.getCurrentContent();

          finalContentState = Modifier.applyEntity(content, selection, entityKey);
          finalChangeType = 'apply-entity'
      } else {
        finalContentState = content.mergeEntityData(entityKey, {
          note_id: data['note_id'],
          text: data['text']
        });
        finalChangeType = 'merge-entity-data'
      }

      const nextState = EditorState.push(editorState, finalContentState, finalChangeType);
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

class FootnoteDecorator extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
          showTooltipAt: null,
        };

        this.onEdit = this.onEdit.bind(this);
        this.onRemove = this.onRemove.bind(this);
        this.openTooltip = this.openTooltip.bind(this);
        this.closeTooltip = this.closeTooltip.bind(this);
    }

    onEdit(e) {
        const { onEdit, entityKey } = this.props;
        e.preventDefault();
        e.stopPropagation();
        onEdit(entityKey);
    }

    onRemove(e) {
        e.preventDefault();
        e.stopPropagation();
        const { onRemove, entityKey, contentState } = this.props;
        const data = contentState.getEntity(entityKey).getData();
        const editor = document.querySelector(`.${data.note_id}`)
                        .closest('[data-streamfield-widget]')
                        .getElementsByTagName('input')[0]
                        .draftailEditor;
        onRemove(entityKey);
        setTimeout(function(){
          const editorState = editor.getEditorState();
          const content = editorState.getCurrentContent();
          const selection = editorState.getSelection();
          const newContentState = Modifier.removeRange(content, selection);
          const newEditorState = EditorState.push(editorState, newContentState, 'remove-range');
          editor.onChange(newEditorState);
        },10);
    }

    openTooltip(e) {
        const trigger = e.target.closest('[data-draftail-trigger]');
        // Click is within the tooltip.
        if (!trigger) { return; }

        const container = trigger.closest('[data-draftail-editor-wrapper]');
        const containerRect = container.getBoundingClientRect();
        const rect = trigger.getBoundingClientRect();

        this.setState({
          showTooltipAt: {
            container: container,
            top: rect.top - containerRect.top - (document.documentElement.scrollTop || document.body.scrollTop),
            left: rect.left - containerRect.left - (document.documentElement.scrollLeft || document.body.scrollLeft),
            width: rect.width,
            height: rect.height,
          },
        });
    }

    closeTooltip() {
        this.setState({ showTooltipAt: null });
    }

    render() {
      var { entityKey, contentState, children } = this.props;
      const data = contentState.getEntity(entityKey).getData();
      const { showTooltipAt } = this.state;

      const summary = React.createElement('div', {
        id: entityKey,
        className: 'footnoteTooltipText',
      }, `${ data.text.split(/\s+/).slice(0,8).join(' ') }${data.text.length > 8 ? '...' : ''}`);

      const editButton = React.createElement('button', {
        className: 'button footnoteButton Tooltip__button',
        onClick: this.onEdit,
      }, 'Edit');

      const removeButton = React.createElement('button', {
        className: 'button button-secondary no Tooltip__button',
        onClick: this.onRemove,
      }, 'Remove');

      const tooltip = React.createElement(window.draftail.Tooltip, {
        target: showTooltipAt,
        direction: 'top',
      }, [summary, editButton, removeButton]);

      return React.createElement('a', {
        role: 'button',
        onMouseUp: this.openTooltip,
        className: `footnoteEntity ${data.note_id}`,
        title: data.text,
        'data-draftail-trigger': true,
      }, ['✱', (showTooltipAt && React.createElement(window.wagtail.components.Portal, {
        node: showTooltipAt.container,
        onClose: this.closeTooltip,
        closeOnClick: true,
        closeOnType: true,
        closeOnResize: true,
      }, tooltip))]);
    }
}

window.draftail.registerPlugin({
    type: 'FOOTNOTE',
    source: FootnoteSource,
    decorator: FootnoteDecorator,
});
