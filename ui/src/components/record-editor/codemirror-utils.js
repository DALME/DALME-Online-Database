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
import { closeBrackets } from "@codemirror/autocomplete";
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
  keymap.of([...defaultKeymap, ...searchKeymap, ...historyKeymap]),
];

export const createEditorState = (doc) => {
  console.log("creation editor state");
  return EditorState.create({
    doc: doc,
    extensions: baseExtensions,
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

// const VueCodemirror = defineComponent({
//   name: "VueCodemirror",
//   props: {
//     autofocus: {
//       type: Boolean,
//       default: true,
//     },
//     disabled: {
//       type: Boolean,
//       default: false,
//     },
//     indentWithTab: {
//       type: Boolean,
//       default: true,
//     },
//     tabSize: {
//       type: Number,
//       default: 4,
//     },
//     placeholder: {
//       type: String,
//       default: "",
//     },
//     autoDestroy: {
//       type: Boolean,
//       default: true,
//     },
//     extensions: Array,
//     lineNumbers: Boolean,
//     lineWrapping: Boolean,
//     visualTags: Boolean,
//     autoCompletion: Boolean,
//     highlightSelection: Boolean,
//     allowMultipleSelections: Boolean,
//     editorTooltips: Boolean,
//     style: Object,
//     phrases: Object,
//     // codemirror options
//     root: Object,
//     selection: Object,
//     modelValue: {
//       type: String,
//       default: "",
//     },
//   },
//   emits: ["change", "update", "focus", "blur", "ready", "update:modelValue"],
//   setup(props, context) {
//     const container = shallowRef();
//     const state = shallowRef();
//     const view = shallowRef();
//     const config = computed(() =>
//       Object.keys(toRaw(props))
//         .filter((key) => key !== "modelValue")
//         .reduce((obj, key) => {
//           obj[key] = props[key];
//           return obj;
//         }, {}),
//     );

//     onMounted(() => {
//       state.value = createEditorState({
//         doc: props.modelValue,
//         selection: config.value.selection,
//         // initialize base extensions only
//         extensions: baseExtensions,
//         onFocus: (viewUpdate) => context.emit("focus", viewUpdate),
//         onBlur: (viewUpdate) => context.emit("blur", viewUpdate),
//         onUpdate: (viewUpdate) => context.emit("update", viewUpdate),
//         onChange: (newDoc, viewUpdate) => {
//           if (newDoc !== props.modelValue) {
//             context.emit("change", newDoc, viewUpdate);
//             context.emit("update:modelValue", newDoc, viewUpdate);
//           }
//         },
//       });

//       view.value = createEditorView({
//         state: state.value,
//         parent: container.value,
//         root: config.value.root,
//       });

//       const editorTools = getEditorTools(view.value);

//       // watch prop.modelValue
//       watch(
//         () => props.modelValue,
//         (newValue) => {
//           if (newValue !== editorTools.getDoc()) {
//             editorTools.setDoc(newValue);
//           }
//         },
//       );

//       // watch prop.extensions
//       watch(
//         () => props.extensions,
//         (extensions) => {
//           console.log("watcher: props.extensions", extensions);
//           editorTools.reExtensions(extensions || []);
//         },
//         { immediate: true },
//       );

//       // watch prop.disabled
//       watch(
//         () => config.value.disabled,
//         (disabled) => editorTools.toggleDisabled(disabled),
//         { immediate: true },
//       );

//       // watch prop.indentWithTab
//       watch(
//         () => config.value.indentWithTab,
//         (iwt) => editorTools.toggleIndentWithTab(iwt),
//         { immediate: true },
//       );

//       // watch prop.tabSize
//       watch(
//         () => config.value.tabSize,
//         (tabSize) => editorTools.setTabSize(tabSize),
//         { immediate: true },
//       );

//       // watch prop.phrases
//       watch(
//         () => config.value.phrases,
//         (phrases) => editorTools.setPhrases(phrases || {}),
//         { immediate: true },
//       );

//       // watch prop.placeholder
//       watch(
//         () => config.value.placeholder,
//         (placeholder) => editorTools.setPlaceholder(placeholder),
//         { immediate: true },
//       );

//       // watch prop.style
//       watch(
//         () => config.value.style,
//         (style) => editorTools.setStyle(style),
//         { immediate: true },
//       );

//       // immediate autofocus
//       if (config.value.autofocus) {
//         editorTools.focus();
//       }

//       context.emit("ready", {
//         state: state.value,
//         view: view.value,
//         container: container.value,
//       });
//     });

//     onBeforeUnmount(() => {
//       if (config.value.autoDestroy && view.value) {
//         destroyEditorView(view.value);
//       }
//     });

//     return () => {
//       return h("div", {
//         class: "v-codemirror",
//         style: { display: "contents" },
//         ref: container,
//       });
//     };
//   },
// });

// export const Codemirror = VueCodemirror;
