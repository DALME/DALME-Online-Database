const React = window.React;
// const Modifier = window.DraftJS.Modifier;
// const EditorState = window.DraftJS.EditorState;
// const SelectionState = window.DraftJS.SelectionState;
// const AtomicBlockUtils = window.DraftJS.AtomicBlockUtils;
const ModalWorkflowSource = window.draftail.ModalWorkflowSource;
const TooltipEntity = window.draftail.TooltipEntity;
// const ChooserModalOnloadHandlerFactory = window.ChooserModalOnloadHandlerFactory;

// const getSelectedBlocksList = (editorState) => {
//   const selectionState = editorState.getSelection();
//   const content = editorState.getCurrentContent();
//   const startKey = selectionState.getStartKey();
//   const endKey = selectionState.getEndKey();
//   const blockMap = content.getBlockMap();
//   const blocks = blockMap
//     .toSeq()
//     .skipUntil((_, k) => k === startKey)
//     .takeUntil((_, k) => k === endKey)
//     .concat([[endKey, blockMap.get(endKey)]]);
//   return blocks.toList();
// };

// const getSelectionText = (editorState) => {
//   const selection = editorState.getSelection();
//   let start = selection.getAnchorOffset();
//   let end = selection.getFocusOffset();
//   const selectedBlocks = getSelectedBlocksList(editorState);

//   if (selection.getIsBackward()) {
//     const temp = start;
//     start = end;
//     end = temp;
//   }

//   let selectedText = '';
//   for (let i = 0; i < selectedBlocks.size; i += 1) {
//     const blockStart = i === 0 ? start : 0;
//     const blockEnd =
//       i === selectedBlocks.size - 1
//         ? end
//         : selectedBlocks.get(i).getText().length;
//     selectedText += selectedBlocks.get(i).getText().slice(blockStart, blockEnd);
//   }

//   return selectedText;
// };

class ReferenceModalWorkflowSource extends ModalWorkflowSource {
  getChooserConfig() {
    return {
      url: window.chooserUrls.referenceChooser,
      urlParams: {},
      onload: window.CHOOSER_MODAL_ONLOAD_HANDLERS,
      responses: {
        chosen: this.onChosen,
      },
    };
  }
}


const Reference = (props) => {
  const { entityKey, contentState } = props;
  console.log(props);
  const data = contentState.getEntity(entityKey).getData();
  console.log(data);
  // return window.React.createElement(
  //   'a',
  //   {
  //     role: 'button',
  //     onMouseUp: () => {
  //       window.open(data.href);
  //     },
  //   },
  //   props.children,
  // );
  // return <TooltipEntity {...props} {...getLinkAttributes(data)} />;
  return React.createElement(
    TooltipEntity,
    data.reference,
    props.children,
  )
};

// Register the plugin directly on script execution so the editor loads it when initialising.
window.draftail.registerPlugin({
  type: 'REFERENCE',
  source: ReferenceModalWorkflowSource,
  decorator: Reference,
}, 'entityTypes');

if (typeof(window.cite) == 'undefined') {
  window.cite = require('citation-js');
}

window.format_reference = (link_id, data) => {
  const link = document.getElementById(link_id);
  const citation = new window.cite(data);
  link.dataset.label = citation.format('citation', { format: 'text', template: 'apa', lang: 'en-US' });
  link.innerHTML = citation.format('bibliography', { format: 'html', template: 'apa', lang: 'en-US' });
} 
