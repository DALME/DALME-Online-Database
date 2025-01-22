<template>
  <div class="bg-grey-2 q-px-sm row justify-between items-center">
    <div class="column q-pt-xs">
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
    <div class="column">
      <div class="row text-grey-7">
        <q-btn flat icon="text_decrease" class="md-editor-button" />
        <q-btn flat icon="text_increase" class="md-editor-button" />
        <q-btn flat icon="undo" class="md-editor-button" />
        <q-btn flat icon="redo" class="md-editor-button" />
        <q-btn flat icon="settings" class="md-editor-button" />
        <q-btn
          flat
          class="md-editor-button"
          icon="code"
          :icon-right="view.showTagMenu ? 'arrow_drop_up' : 'arrow_drop_down'"
          @click="view.showTagMenu = !view.showTagMenu"
        />
      </div>
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
        <Codemirror
          v-model="editorContent"
          placeholder="Start transcription..."
          :style="{ height: `${editorHeight}px`, width: `${editorWidth}px` }"
          :extensions="extensions"
          :options="options"
          @ready="editorReady"
        />
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
  h,
  onMounted,
  render,
  ref,
  shallowRef,
  watch,
} from "vue";
import { useStores } from "@/use";
import { TeiRenderer } from "@/components";
import { Codemirror } from "./codemirror.js";
import {
  Decoration,
  EditorView,
  ViewPlugin,
  keymap,
  highlightSpecialChars,
  drawSelection,
  highlightActiveLine,
  dropCursor,
  rectangularSelection,
  crosshairCursor,
  lineNumbers,
  highlightActiveLineGutter,
} from "@codemirror/view";
import {
  defaultHighlightStyle,
  syntaxHighlighting,
  indentOnInput,
  bracketMatching,
  foldGutter,
} from "@codemirror/language";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { searchKeymap, highlightSelectionMatches } from "@codemirror/search";
import { autocompletion, closeBrackets } from "@codemirror/autocomplete";
// import { syntaxTree } from "@codemirror/language";
// import { RangeSet } from "@codemirror/state";
import { xml } from "@codemirror/lang-xml";
import { oneDark } from "@codemirror/theme-one-dark";
import TeiSidebar from "./TeiSidebar.vue";
import ContextMenu from "./ContextMenu.vue";
import TeiTag from "./TeiTag.vue";
import { TagDecorator } from "./tei-tag-extension.js";

export default defineComponent({
  name: "TeiEditor",
  components: {
    Codemirror,
    ContextMenu,
    TeiRenderer,
    TeiSidebar,
  },
  setup() {
    const { currentPageData, view } = useStores();
    const { editorHeight, editorWidth } = inject("editorDimensions");
    const disabled = computed(() => isEmpty(currentPageData.value.tei));
    const currentInstance = getCurrentInstance();
    const editor = shallowRef();
    const editorContent = currentPageData.value.tei;
    const widgetTracker = ref([]);
    const tagComponents = ref([]);
    const changeQueue = ref([]);
    const updatingEditor = ref(false);

    const editorReady = (payload) => (editor.value = payload.view);

    const updateTag = (changes) => {
      console.log("updateTag", changes);
      editor.value.dispatch({ changes });
    };

    const tagMatcher = new TagDecorator(widgetTracker, changeQueue);
    // const tagMatcher = new TagDecorator();

    // const renderWidgets = (decorations) => {
    //   console.log("rendering widgets", decorations);
    //   for (let iter = decorations.iter(); iter.value !== null; iter.next()) {
    //     const widget = iter.value.widget;
    //     const compId = crypto.randomUUID().replace(/-/g, "");
    //     const component = h(TeiTag, {
    //       tag: widget.tag,
    //       attributes: widget.attributes,
    //       type: widget.type,
    //       tagData: widget.tagData,
    //       eData: widget.eData,
    //       onUpdate: updateTag,
    //     });
    //     component.key = compId;
    //     component.appContext = currentInstance.appContext.app._context;
    //     widget.container.setAttribute("id", compId);
    //     console.log(`rendering ${compId}`);
    //     render(component, widget.container);
    //   }
    // };

    // const tagPlugin = ViewPlugin.fromClass(
    //   class {
    //     constructor(view) {
    //       this.tags = tagMatcher.createDeco(view);
    //       renderWidgets(this.tags);
    //     }

    //     destroy() {
    //       console.log("destroying tagPlugin");
    //     }

    //     update(update) {
    //       if (
    //         update.docChanged ||
    //         update.viewportChanged ||
    //         syntaxTree(update.startState) != syntaxTree(update.state)
    //       ) {
    //         this.tags = tagMatcher.createDeco(view);
    //         renderWidgets(this.tags);
    //       }
    //     }
    //   },
    //   {
    //     decorations: (instance) => instance.tags,
    //     provide: (plugin) =>
    //       EditorView.atomicRanges.of((view) => {
    //         return view.plugin(plugin)?.tags || Decoration.none;
    //       }),
    //   },
    // );

    const renderWidgets = () => {
      const widgetEls = document.querySelectorAll(".cm-tag-widget-container");
      // console.log("renderWidgets", widgetEls);
      widgetEls.forEach((el) => {
        // console.log("processing", el);
        const compId = el.getAttribute("id") || crypto.randomUUID().replace(/-/g, "");
        // console.log("compId", compId);
        if (!tagComponents.value.includes(compId)) {
          const widgetId = el.getAttribute("data-widget");
          const widgetEntry = widgetTracker.value.find((x) => x.widgets.includes(widgetId));
          if (widgetEntry) {
            widgetEntry["component"] = compId;
            const component = h(TeiTag, {
              id: compId,
              tag: widgetEntry.data.tag,
              attributes: widgetEntry.data.attributes,
              type: widgetEntry.data.type,
              tagData: widgetEntry.data.tagData,
              eData: widgetEntry.data.eData,
              pairing: widgetEntry.data.pairing,
              anchor: el,
              tracker: widgetTracker,
              onUpdate: updateTag,
            });
            component.key = compId;
            component.appContext = currentInstance.appContext.app._context;
            tagComponents.value.push(compId);
            el.setAttribute("id", compId);
            console.log(`rendering ${compId}`);
            render(component, el);
          } else {
            console.log(`no widget entry for ${widgetId}`);
          }
        } else {
          console.log(`component ${compId} already rendered`);
        }
      });
    };

    // eslint-disable-next-line unused-imports/no-unused-vars
    const tagPlugin = ViewPlugin.fromClass(
      class {
        constructor(view) {
          this.tags = Decoration.none;
          this.create(view);
        }

        async create(view) {
          this.tags = tagMatcher.createDeco(view);
          await nextTick();
          renderWidgets();
        }

        destroy() {
          console.log("destroying tagPlugin");
        }

        async update(update) {
          if (update.docChanged || update.viewportChanged) {
            updatingEditor.value = true;
            this.tags = await tagMatcher.updateDeco(update, this.tags);
            updatingEditor.value = false;
            renderWidgets();
          }
        }
      },
      {
        decorations: (instance) => instance.tags,
        provide: (plugin) =>
          EditorView.atomicRanges.of((view) => {
            return view.plugin(plugin)?.tags || Decoration.none;
          }),
      },
    );

    const extensions = [
      xml(),
      oneDark,
      tagPlugin,
      EditorView.lineWrapping,
      lineNumbers(),
      highlightActiveLineGutter(),
      highlightSpecialChars(),
      history(),
      foldGutter(),
      drawSelection(),
      dropCursor(),
      indentOnInput(),
      syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
      bracketMatching(),
      closeBrackets(),
      autocompletion(),
      rectangularSelection(),
      crosshairCursor(),
      highlightActiveLine(),
      highlightSelectionMatches(),
      keymap.of([...defaultKeymap, ...searchKeymap, ...historyKeymap]),
    ];

    const options = {
      lineWrapping: true,
    };

    const onTabSwitch = (value) => {
      // if (value === "preview") currentPageData.value.tei = editor.getValue();
      console.log(`Switching tab to ${value}`);
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
      if (!isNil(editor)) {
        editor.value.requestMeasure();
      }
    });

    // watch(
    //   changeQueue,
    //   async () => {
    //     if (changeQueue.value.length) {
    //       await nextTick();
    //       console.log("watch changeQueue", changeQueue.value);
    //       changeQueue.value.forEach((change) => {
    //         updateTag(change);
    //       });
    //       changeQueue.value = [];
    //     }
    //   },
    //   { deep: true },
    // );

    onMounted(async () => {
      view.value.editorTab = "write";
      currentPageData.value.editOn = true;
      window.testEditor = editor.value;
    });

    return {
      editor,
      editorReady,
      extensions,
      editorContent,
      currentPageData,
      disabled,
      editorHeight,
      editorWidth,
      onTabSwitch,
      view,
      options,
      // insertTag,
    };
  },
});
</script>

<style lang="scss">
.editor-panel {
  padding: 0;
  background: linear-gradient(120deg, #fefefe, #efefef) no-repeat 0px/40px 100%;
}
.ͼ1 .cm-scroller {
  line-height: 2;
  font-family: "Menlo", "Consolas", "Monaco", monospace;
}
</style>
