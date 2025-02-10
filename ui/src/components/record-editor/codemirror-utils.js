import { EditorState, Compartment, StateEffect } from "@codemirror/state";
import {
  EditorView,
  keymap,
  placeholder,
  drawSelection,
  highlightActiveLine,
  dropCursor,
  highlightActiveLineGutter,
} from "@codemirror/view";
import {
  indentUnit,
  defaultHighlightStyle,
  syntaxHighlighting,
  bracketMatching,
  foldGutter,
} from "@codemirror/language";
import { lintGutter } from "@codemirror/lint";
import { indentWithTab, defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { searchKeymap } from "@codemirror/search";
import { closeBrackets, completionKeymap } from "@codemirror/autocomplete";
import { xml } from "@codemirror/lang-xml";

export const baseExtensions = [
  xml(),
  syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
  highlightActiveLineGutter(),
  highlightActiveLine(),
  history(),
  bracketMatching(),
  foldGutter(),
  dropCursor(),
  closeBrackets(),
  lintGutter(),
  drawSelection(),
  placeholder("Start transcription..."),
  keymap.of([...defaultKeymap, ...searchKeymap, ...historyKeymap, ...completionKeymap]),
];

export const createEditorState = ({ doc, onUpdate, onChange, onFocus, onBlur }) => {
  console.log("creation editor state");
  return EditorState.create({
    doc: doc,
    extensions: [
      ...baseExtensions,
      EditorView.updateListener.of((viewUpdate) => {
        // https://discuss.codemirror.net/t/codemirror-6-proper-way-to-listen-for-changes/2395/11
        onUpdate(viewUpdate);
        // doc changed
        if (viewUpdate.docChanged) {
          onChange(viewUpdate.state.doc.toString(), viewUpdate);
        }
        // focus state change
        if (viewUpdate.focusChanged) {
          viewUpdate.view.hasFocus ? onFocus(viewUpdate) : onBlur(viewUpdate);
        }
      }),
    ],
  });
};

export const createEditorView = (config) => new EditorView({ ...config });
export const destroyEditorView = (view) => view.destroy();

// https://codemirror.net/examples/config/
// https://github.com/uiwjs/react-codemirror/blob/22cc81971a/src/useCodeMirror.ts#L144
// https://gist.github.com/s-cork/e7104bace090702f6acbc3004228f2cb
const createEditorCompartment = (view) => {
  const compartment = new Compartment();
  const run = (extension) => {
    // view.dispatch({ effects: compartment.reconfigure(extension) });
    compartment.get(view.state)
      ? view.dispatch({ effects: compartment.reconfigure(extension) }) // reconfigure
      : view.dispatch({
          effects: StateEffect.appendConfig.of(compartment.of(extension)),
        }); // inject
  };
  return { compartment, run };
};

// https://codemirror.net/examples/reconfigure/
const createEditorExtensionToggler = (view, extension) => {
  const { compartment, run } = createEditorCompartment(view);
  return (targetApply) => {
    const exExtension = compartment.get(view.state);
    const apply = targetApply ?? exExtension !== extension;
    run(apply ? extension : []);
  };
};

export const getEditorTools = (view) => {
  // doc state
  const getDoc = () => view.state.doc.toString();
  const setDoc = (newDoc) => {
    if (newDoc !== getDoc()) {
      view.dispatch({
        changes: {
          from: 0,
          to: view.state.doc.length,
          insert: newDoc,
        },
      });
    }
  };

  // UX operations
  const focus = () => view.focus();

  // reconfigure extension
  const { run: reExtensions } = createEditorCompartment(view);

  // disabled editor
  const toggleDisabled = createEditorExtensionToggler(view, [
    EditorView.editable.of(false),
    EditorState.readOnly.of(true),
  ]);

  // https://codemirror.net/examples/tab/
  const toggleIndentWithTab = createEditorExtensionToggler(view, keymap.of([indentWithTab]));

  // tab size
  // https://gist.github.com/s-cork/e7104bace090702f6acbc3004228f2cb
  const { run: reTabSize } = createEditorCompartment(view);
  const setTabSize = (tabSize) => {
    reTabSize([EditorState.tabSize.of(tabSize), indentUnit.of(" ".repeat(tabSize))]);
  };

  // phrases
  // https://codemirror.net/examples/translate/
  const { run: rePhrases } = createEditorCompartment(view);
  const setPhrases = (phrases) => {
    rePhrases([EditorState.phrases.of(phrases)]);
  };

  // set editor's placeholder
  const { run: rePlaceholder } = createEditorCompartment(view);
  const setPlaceholder = (value) => {
    rePlaceholder(placeholder(value));
  };

  // set style to editor element
  // https://codemirror.net/examples/styling/
  const { run: reStyle } = createEditorCompartment(view);
  const setStyle = (style = {}) => {
    reStyle(EditorView.theme({ "&": { ...style } }));
  };

  return {
    focus,
    getDoc,
    setDoc,
    reExtensions,
    toggleDisabled,
    toggleIndentWithTab,
    setTabSize,
    setPhrases,
    setPlaceholder,
    setStyle,
  };
};
