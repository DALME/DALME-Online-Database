<template>
  <div class="bg-grey-2 q-px-sm row justify-between items-center">
    <div class="column q-pt-xs">
      <!--q-btn @click="test" label="Test" /-->
      <q-tabs
        v-model="view.editorTab"
        dense
        shrink
        class="text-grey md-editor-tabs"
        active-color="light-blue-10"
        active-bg-color="white"
        indicator-color="transparent"
        align="left"
        narrow-indicator
        no-caps
        content-class="q-px-sm"
        @update:model-value="onTabSwitch"
      >
        <q-tab name="write" label="Write" />
        <q-tab name="preview" label="Preview" :disable="disabled" />
      </q-tabs>
    </div>
    <q-btn @click="parse" label="parse" />
    <div class="column">
      <ToolBar />
    </div>
  </div>
  <q-separator />
  <q-tab-panels
    v-model="view.editorTab"
    keep-alive
    keep-alive-exclude="TeiRenderer"
    animated
    transition-prev="jump-up"
    transition-next="jump-up"
    class="editor-panel text-body2"
    :style="`height: ${editorHeight}px;`"
  >
    <q-tab-panel name="write" class="row q-pa-none">
      <div class="col">
        <div class="v-codemirror editor-container" ref="container"></div>
      </div>
      <TeiSidebar />
      <ContextMenu />
    </q-tab-panel>
    <q-tab-panel name="preview" class="render-panel" :style="`height: ${editorHeight}px`">
      <TeiRenderer :text="currentPageData.tei" />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script>
import { isEmpty, isNil } from "ramda";
import {
  computed,
  defineComponent,
  inject,
  nextTick,
  getCurrentInstance,
  onBeforeUnmount,
  onMounted,
  ref,
  shallowRef,
  watch,
} from "vue";
import { useStores } from "@/use";
import { TeiRenderer } from "@/components";
import {
  createEditorState,
  createEditorView,
  destroyEditorView,
  getEditorTools,
} from "./codemirror-utils.js";
import { EditorState } from "@codemirror/state";
import { EditorView, lineNumbers, tooltips } from "@codemirror/view";
import { highlightSelectionMatches } from "@codemirror/search";
import { autocompletion } from "@codemirror/autocomplete";
import TeiSidebar from "./TeiSidebar.vue";
import ContextMenu from "./ContextMenu.vue";
import ToolBar from "./ToolBar.vue";
import { tagDecoratorPlugin } from "./tag-decorator.js";
import * as themes from "./themes.js";
import { syntaxTree } from "@codemirror/language";

export default defineComponent({
  name: "TeiEditor",
  components: {
    ContextMenu,
    TeiRenderer,
    TeiSidebar,
    ToolBar,
  },
  setup() {
    const { currentPageData, view, settings, preferences } = useStores();
    const { editorHeight, editorWidth } = inject("editorDimensions");
    const disabled = computed(() => isEmpty(currentPageData.value.tei));
    const currentInstance = getCurrentInstance();
    const container = shallowRef();
    const editorState = shallowRef();
    const editorView = shallowRef();

    const widgetRegistry = ref({});
    const componentRegistry = ref({});
    const currentTheme = computed(() =>
      preferences.value.theme.value ? themes[preferences.value.theme.value] : themes["oneDark"],
    );

    // editorView.value.updateState: 0 = Idle, 1 = Measuring, 2 = Updating
    // eslint-disable-next-line unused-imports/no-unused-vars
    const updateTag = (changes) => {
      console.log("updateTag", changes, editorView.value.updateState);
      if (editorView.value.updateState !== 0) {
        Promise.resolve().then(() => editorView.value.dispatch({ changes }));
      } else {
        editorView.value.dispatch({ changes });
      }
    };

    const cleanUp = (evt) => {
      console.log("cleanUp", evt, evt.detail, editorView.value.updateState);
      const paired = document.querySelectorAll(`[data-id="${evt.detail.id}"]`);
      console.log("paired", paired);
      if (paired.length) {
        paired.forEach((node) => {
          if (node.hasAttribute("id")) {
            const from = node.getAttribute("data-from");
            const to = node.getAttribute("data-to");
            console.log("contents", editorState.value.doc.sliceString(from, to));
            updateTag({ from, to });
          }
        });
      }
    };

    const parse = () => {
      syntaxTree(editorState.value).iterate({
        enter: (node) => {
          // if (cursor.name === "MissingCloseTag") {
          if (node.node.name === "OpenTag") {
            console.log(node.node.node);
          }
        },
      });
    };

    const tagPlugin = tagDecoratorPlugin(
      currentInstance,
      updateTag,
      widgetRegistry,
      componentRegistry,
    );

    window.testPlug = tagPlugin;

    const extensions = computed(() => {
      console.log("generating extensions");
      const payload = [];
      payload.push(currentTheme.value);
      if (preferences.value.visualTags.value) {
        payload.push(tagPlugin);
      }
      if (preferences.value.lineNumbers.value) payload.push(lineNumbers());
      if (preferences.value.lineWrapping.value) payload.push(EditorView.lineWrapping);
      if (preferences.value.autoCompletion.value) payload.push(autocompletion());
      if (preferences.value.highlightSelection.value) payload.push(highlightSelectionMatches());
      if (preferences.value.allowMultipleSelections.value) {
        payload.push(EditorState.allowMultipleSelections.of(true));
      }
      if (preferences.value.editorTooltips.value) payload.push(tooltips());
      return payload;
    });

    const style = computed(() => ({
      height: `${editorHeight}px`,
      width: `${editorWidth}px`,
      "font-size": `${preferences.value.fontSize.value}px`,
    }));

    const onTabSwitch = (value) => {
      // if (value === "preview") currentPageData.value.tei = editor.getValue();
      console.log(`Switching tab to ${value}`);
    };

    // eslint-disable-next-line unused-imports/no-unused-vars
    const insertTag = (el, evt) => {
      console.log("insertTag", el, evt);
      const selection = editorView.value.state.selection.main;
      const selectionText = editorView.value.state.doc.sliceString(selection.from, selection.to);
      const isCompound = el.compound;
      const label = el.label;
      const tags = el.tags.map((x) => settings.tags.get(x));
      const changes = [];
      if (!isCompound && tags.length === 1) {
        const tag = tags[0];
        let result = `<${tag.name}`;
        for (const attr of tag.attributes) {
          if (attr.required && !attr.editable) {
            result += ` ${attr.value}="${attr.default}"`;
          }
        }
        result += `>${selectionText}</${tag.name}>`;
        changes.push({ from: selection.from, to: selection.to, insert: result });
      }
      console.log(selection, selectionText, changes, isCompound, tags, label);
      editorView.value.dispatch({ changes });
    };
    // const insertTag = (type, tag, attributes) => {
    //   let tagAtt = [];
    //   let spAtt = {};

    //   if (attributes) {
    //     attributes = attributes.includes("-") ? attributes.split("-") : [attributes];

    //     attributes.forEach((attribute) => {
    //       let att = attribute.split("|");
    //       if (att.length === 2) {
    //         tagAtt.push([att[0], att[1]]);
    //       } else {
    //         let att_value;
    //         // if (att[1] === "text") {
    //         //   att_value = $("#"+att[2]).val();
    //         //   $("#"+att[2]).val("");
    //         // }
    //         // if (att[1] === "choice") {
    //         //   att_value = $("#"+att[2]).find("option:selected").text();
    //         //   $("#"+att[2])[0].selectedIndex = 0;
    //         // }

    //         if (tag === "note" || tag === "seg") {
    //           spAtt[att[0]] = att_value;
    //         } else {
    //           tagAtt.push([att[0], att_value]);
    //         }
    //       }
    //     });
    //   }

    //   if (tag === "seg") {
    //     tagAtt.push(["target", spAtt["target"]]);
    //     tagAtt.push(["rend", spAtt["rend"]]);
    //   }

    //   if (tag === "note") {
    //     if (spAtt["type"] === "renvoi") {
    //       /* eslint-disable */
    //       const noteRef = `<ref target="${spAtt["target"]}"/>`;
    //       const noteOutput = `\n\n<note xml:id="${spAtt["target"]}">${spAtt["text"]}</note>`;
    //       /* eslint-enable */
    //       editor.session.insert(editor.getCursorPosition(), noteRef);
    //       editor.session.insert(
    //         {
    //           row: editor.session.getLength(),
    //           column: 0,
    //         },
    //         noteOutput,
    //       );
    //     } else {
    //       /* eslint-disable */
    //       const tagOutput = `<note type="${spAtt["type"]}">${spAtt["text"]}</note>`;
    //       /* eslint-enable */
    //       editor.session.insert(editor.getCursorPosition(), tagOutput);
    //     }
    //   } else {
    //     let tagOutput = "<" + tag;

    //     if (tagAtt.length !== 0) {
    //       tagAtt.forEach((attribute) => {
    //         if (attribute[1] !== "" && attribute[1] !== "Join") {
    //           tagOutput += " " + attribute[0] + '="' + attribute[1] + '"'; // eslint-disable-line
    //         }
    //       });
    //     }

    //     if (type === "w") {
    //       const range = editor.selection.getRange();
    //       tagOutput += ">" + editor.getSelectedText() + "</" + tag + ">";
    //       editor.session.replace(range, tagOutput);
    //     } else {
    //       tagOutput += "/>";
    //       editor.session.insert(editor.getCursorPosition(), tagOutput);
    //     }

    //     if (tag === "seg") {
    //       /* eslint-disable */
    // eslint-disable-next-line max-len
    //       const noteOutput = `\n\n<note type="brace" xml:id="${spAtt["target"]}">${spAtt["text"]}</note>`;
    //       /* eslint-enable */
    //       editor.session.insert(
    //         {
    //           row: editor.session.getLength(),
    //           column: 0,
    //         },
    //         noteOutput,
    //       );
    //     }
    //   }
    // };

    watch([editorHeight, editorWidth], async () => {
      await nextTick();
      if (!isNil(editorView)) {
        editorView.value.requestMeasure();
      }
    });

    onMounted(async () => {
      console.log("mounted TEIeditor");
      view.value.editorTab = "write";
      currentPageData.value.editOn = true;
      window.testEditor = currentInstance;
      // window.testEditor = editorView.value;
      editorState.value = createEditorState(currentPageData.value.tei);

      editorView.value = createEditorView({
        state: editorState.value,
        parent: container.value,
      });

      const editorTools = getEditorTools(editorView.value);
      editorTools.focus();

      container.value.addEventListener("widgetDestroyed", cleanUp);

      watch(
        () => currentPageData.value.tei,
        (newValue) => {
          if (newValue !== editorTools.getDoc()) {
            editorTools.setDoc(newValue);
          }
        },
      );

      watch(
        () => extensions.value,
        (extensions) => {
          console.log("watcher: props.extensions", extensions);
          editorTools.reExtensions(extensions || []);
        },
        { immediate: true },
      );

      watch(
        () => disabled.value,
        (disabled) => editorTools.toggleDisabled(disabled),
        { immediate: true },
      );

      watch(
        () => style.value,
        (style) => editorTools.setStyle(style),
        { immediate: true },
      );
    });

    onBeforeUnmount(() => {
      if (editorView.value) {
        destroyEditorView(editorView.value);
      }
    });

    return {
      container,
      currentPageData,
      disabled,
      editorHeight,
      editorWidth,
      onTabSwitch,
      view,
      parse,
    };
  },
});
</script>

<style lang="scss">
.editor-container {
  display: contents;
}
.editor-panel {
  padding: 0;
  background: linear-gradient(120deg, #fefefe, #efefef) no-repeat 0px/40px 100%;
}
.ͼ1 .cm-scroller {
  line-height: 2;
  font-family: "Menlo", "Consolas", "Monaco", monospace;
}
</style>
