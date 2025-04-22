<template>
  <div class="bg-grey-2 q-px-sm row justify-between items-center">
    <div class="column q-pt-xs">
      <q-tabs
        v-model="currentPageData.editorTab"
        @update:model-value="onTabSwitch"
        active-bg-color="white"
        active-color="light-blue-10"
        align="left"
        class="text-grey md-editor-tabs"
        content-class="q-px-sm"
        indicator-color="transparent"
        dense
        narrow-indicator
        no-caps
        shrink
      >
        <q-tab :disable="disabled" label="Preview" name="preview" />
        <q-tab class="editor-tab-edit" label="Edit" name="edit" />
      </q-tabs>
    </div>
    <!--q-btn @click="parse" label="parse" /-->
    <div class="column">
      <transition
        enter-active-class="animated slideInRight"
        leave-active-class="animated slideOutRight"
        appear
      >
        <ToolBar v-show="currentPageData.editorTab === 'edit'" />
      </transition>
    </div>
  </div>
  <q-separator />
  <q-tab-panels
    v-model="currentPageData.editorTab"
    :style="`height: ${editorHeight}px;`"
    class="editor-panel text-body2"
    animated
    keep-alive
  >
    <q-tab-panel class="row q-pa-none" name="edit">
      <div class="col editor-container-col">
        <div ref="container" class="v-codemirror editor-container"></div>
      </div>
      <TeiSidebar />
      <ContextMenu />
    </q-tab-panel>
    <q-tab-panel :style="`height: ${editorHeight}px`" class="render-panel" name="preview">
      <TeiRenderer />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script>
import { autocompletion } from "@codemirror/autocomplete";
import { highlightSelectionMatches } from "@codemirror/search";
import { EditorState } from "@codemirror/state";
import { EditorView, lineNumbers, tooltips } from "@codemirror/view";
import { isEmpty, isNil } from "ramda";
import {
  computed,
  defineComponent,
  getCurrentInstance,
  inject,
  nextTick,
  onBeforeUnmount,
  onMounted,
  provide,
  shallowRef,
  watch,
} from "vue";

import { TeiRenderer } from "@/components";
import { useEventHandling, useStores } from "@/use";

import {
  createEditorState,
  createEditorView,
  destroyEditorView,
  getEditorTools,
} from "./codemirror-utils.js";
import ContextMenu from "./ContextMenu.vue";
import { tagDecoratorPlugin } from "./tag-decorator.js";
import TeiSidebar from "./TeiSidebar.vue";
import * as themes from "./themes.js";
import ToolBar from "./ToolBar.vue";
import { getCompletions } from "./transcription-tools.js";

export default defineComponent({
  name: "TeiEditor",
  components: {
    ContextMenu,
    TeiRenderer,
    TeiSidebar,
    ToolBar,
  },
  setup() {
    const { currentPageData, view, preferences, settings } = useStores();
    const { eventBus } = useEventHandling();
    const { editorHeight, editorWidth } = inject("editorDimensions");
    const disabled = computed(() => isEmpty(currentPageData.value.tei));
    const currentInstance = getCurrentInstance();
    const container = shallowRef();
    const editorState = shallowRef();
    const editorView = shallowRef();
    const editorTools = shallowRef();

    const currentTheme = computed(() =>
      preferences.value.theme.value ? themes[preferences.value.theme.value] : themes["oneDark"],
    );

    const editorBackground = computed(() => {
      const themeOpts = settings.getOptions("theme");
      return themeOpts.find((x) => x.value == preferences.value.theme.value).bg;
    });

    // editorView.value.updateState: 0 = Idle, 1 = Measuring, 2 = Updating
    const updateTag = (changes) => {
      console.log("updateTag", changes, editorView.value.updateState);
      if (editorView.value.updateState !== 0) {
        Promise.resolve().then(() => editorView.value.dispatch({ changes }));
      } else {
        editorView.value.dispatch({ changes });
      }
    };

    const onEditorUpdate = (_update) => {
      console.log("Editor update:");
    };
    const onEditorFocus = (_update) => {
      console.log("Editor focus:");
    };
    const onEditorBlur = (_update) => {
      console.log("Editor blur:");
    };
    const onEditorChange = (newDoc, _update) => {
      if (newDoc !== currentPageData.value.tei) {
        currentPageData.value.tei = newDoc;
      }
    };

    const tagPlugin = tagDecoratorPlugin(currentInstance, updateTag);

    const extensions = computed(() => {
      console.log("generating extensions");
      const payload = [];
      payload.push(currentTheme.value);
      if (preferences.value.visualTags.value) {
        payload.push(tagPlugin);
      }
      if (preferences.value.lineNumbers.value) payload.push(lineNumbers());
      if (preferences.value.lineWrapping.value) payload.push(EditorView.lineWrapping);
      if (preferences.value.editorTooltips.value) {
        payload.push(
          tooltips({
            position: "absolute",
            parent: container.value,
          }),
        );
      }
      if (preferences.value.autoCompletion.value) {
        payload.push(autocompletion({ override: [getCompletions] }));
      }
      if (preferences.value.highlightSelection.value) payload.push(highlightSelectionMatches());
      if (preferences.value.allowMultipleSelections.value) {
        payload.push(EditorState.allowMultipleSelections.of(true));
      }
      return payload;
    });

    const style = computed(() => ({
      height: `${editorHeight}px`,
      width: `${editorWidth}px`,
      "font-size": `${preferences.value.fontSize.value}px`,
    }));

    const onTabSwitch = (value) => {
      if (value === "preview") {
        currentPageData.value.tei = editorTools.value.getDoc();
      } else {
        editorTools.value.setDoc(currentPageData.value.tei);
        // editorView.value.requestMeasure();
      }
    };

    // eslint-disable-next-line unused-imports/no-unused-vars
    const insertTag = (el, evt) => {
      console.log("insertTag", el, evt);
      // const selection = editorView.value.state.selection.main;
      // const selectionText = editorView.value.state.doc.sliceString(selection.from, selection.to);
      // const isCompound = el.compound;
      // const label = el.label;
      // const tags = el.tags.map((x) => settings.tags.get(x));
      // const changes = [];
      // if (!isCompound && tags.length === 1) {
      //   const tag = tags[0];
      //   let result = `<${tag.name}`;
      //   for (const attr of tag.attributes) {
      //     if (attr.required && !attr.editable) {
      //       result += ` ${attr.value}="${attr.default}"`;
      //     }
      //   }
      //   result += `>${selectionText}</${tag.name}>`;
      //   changes.push({ from: selection.from, to: selection.to, insert: result });
      // }
      // console.log(selection, selectionText, changes, isCompound, tags, label);
      // editorView.value.dispatch({ changes });
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

    onMounted(() => {
      editorState.value = createEditorState({
        doc: currentPageData.value.tei,
        onUpdate: onEditorUpdate,
        onChange: onEditorChange,
        onFocus: onEditorFocus,
        onBlur: onEditorBlur,
      });

      editorView.value = createEditorView({
        state: editorState.value,
        parent: container.value,
      });

      editorTools.value = getEditorTools(editorView.value);
      editorTools.value.focus();

      watch(
        () => currentPageData.value.tei,
        (newValue) => {
          if (newValue !== editorTools.value.getDoc()) {
            editorTools.value.setDoc(newValue);
          }
        },
      );

      watch(
        () => extensions.value,
        (extensions) => {
          editorTools.value.reExtensions(extensions || []);
        },
        { immediate: true },
      );

      watch(
        () => disabled.value,
        (disabled) => editorTools.value.toggleDisabled(disabled),
        { immediate: true },
      );

      watch(
        () => style.value,
        (style) => editorTools.value.setStyle(style),
        { immediate: true },
      );

      const destroyEditor = () => {
        destroyEditorView(editorView.value);
      };

      const updateEditorRendering = () => {
        editorView.value.requestMeasure();
      };

      eventBus.on("updateEditorRendering", updateEditorRendering);
      eventBus.on("destroyEditor", destroyEditor);
    });

    onBeforeUnmount(() => {
      if (editorView.value) {
        destroyEditorView(editorView.value);
      }
    });

    provide("insertTag", insertTag);

    // const test = () => {
    //   console.log("test");
    //   currentPageData.value.tei = "BOO!";
    // };

    // const parse = () => {
    //   // const tree = ensureSyntaxTree(editorState.value, editorState.value.doc.length, 5000);
    //   // const from = editorView.value.viewport.from;
    //   // const to = editorView.value.viewport.to;
    //   // console.log("PARSING:", from, to);
    //   syntaxTree(editorState.value).iterate({
    //     enter: (node) => {
    //       // if (cursor.name === "MissingCloseTag") {
    //       console.log(
    //         node.node.name,
    //         editorState.value.doc.sliceString(node.node.from, node.node.to),
    //         node.node,
    //       );
    //     },
    //   });
    // };

    return {
      container,
      currentPageData,
      disabled,
      editorHeight,
      editorWidth,
      onTabSwitch,
      view,
      editorBackground,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-tabs {
  margin-bottom: -1px;
}
.q-tab {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-top: 1px solid #d1d1d1;
  border-left: 1px solid #d1d1d1;
  border-right: 1px solid #d1d1d1;
  margin-right: -1px;
}
.q-tab .q-focus-helper {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}
.q-tab:last-of-type {
  border-right: 1px solid #d1d1d1;
}
.q-tab-panels.editor-panel {
  transition: height 0.2s ease-in-out;
}
.editor-tab-edit.q-tab--active {
  background-color: v-bind(editorBackground) !important;
  color: #94abd6 !important;
}
.editor-container {
  display: contents;
}
.editor-container-col {
  background-color: v-bind(editorBackground);
}
.editor-panel {
  padding: 0;
}
:deep(.ͼ1 .cm-scroller) {
  line-height: 2;
  font-family: "Menlo", "Consolas", "Monaco", monospace;
}
:deep(.cm-tag-widget-container) {
  display: inline-block;
  margin: 0 5px;
  vertical-align: middle;
}
// .cm-widgetBuffer:first-child + .cm-tag-widget-container {
//   margin-left: 0;
// }
:deep(.cm-tag-widget) {
  border: 2px solid rgb(171 178 191);
  border-radius: 6px;
  height: 20px;
  min-width: 22px;
  display: flex;
  align-items: center;
}
:deep(.cm-tag-widget .tag-marker) {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding-left: 2px;
  padding-right: 2px;
}
:deep(.cm-tag-widget .tag-marker .tag-text) {
  font-size: 10px;
  font-family: "Roboto";
  font-weight: 400;
}
:deep(.cm-tag-widget.open) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right: none;
}
:deep(.cm-tag-widget.close) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-left: none;
}
:deep(.cm-tag-widget.annotation) {
  border-color: #684545;
  color: #b08181;
  // background-color: #342828;
}
:deep(.cm-tag-widget.editorial) {
  border-color: #3c7072;
  color: #749ba5;
  // background-color: #253335;
}
:deep(.cm-tag-widget.formatting) {
  border-color: #4b6391;
  color: #9eb5e7;
  // background-color: #2b343b;
}
:deep(.cm-tag-widget.layout) {
  border-color: #3d7746;
  color: #71b572;
  // background-color: #273124;
}
:deep(.cm-tag-widget.marks) {
  border-color: #704b91;
  color: #9e73ae;
  // background-color: #362b3b;
}
:deep(.cm-tag-widget.other) {
  border-color: #615f5f;
  color: #9c9797;
  // background-color: #2d2c2c;
}
:deep(.cm-tag-widget.self-close:hover),
:deep(.cm-tag-widget.open:hover) {
  // background-color: #ffffff1a;
  border-color: #ffffffc9;
  color: #e7e3e3;
}
:deep(.cm-tag-widget i) {
  font-size: 10px;
}
</style>
