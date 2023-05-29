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
  >
    <q-tab-panel name="write" class="row q-pa-none">
      <div class="col-grow">
        <div
          id="ace-editor"
          :style="`height: ${editorHeight}px; width: ${editorWidth}px`"
        />
      </div>
      <transition name="collapse">
        <div
          v-if="view.showTagMenu"
          class="col tag-menu"
          :style="`height: ${editorHeight + 20}px`"
        >
          <q-input
            dense
            borderless
            hide-bottom-space
            v-model="tagFilter"
            debounce="300"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            :placeholder="`Filter tags`"
            class="tag-search-box full-width"
          >
            <template v-slot:append>
              <q-icon
                v-if="tagFilter"
                name="close"
                class="cursor-pointer"
                size="12px"
                color="blue-grey-5"
                @click="tagFilter = ''"
              />
            </template>
          </q-input>
          <q-list dense separator>
            <template v-for="(tag, idx) in teiTagsFiltered" :key="idx">
              <q-btn-dropdown
                flat
                no-caps
                auto-close
                split
                align="left"
                :label="tag.name"
                content-class="tag-menu-popup outlined-item menu-shadow"
              >
                <q-list dense separator>
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-detail text-grey-7 q-py-sm">
                        <q-icon
                          name="o_info"
                          size="14px"
                          color="grey-6"
                          class="q-mr-xs"
                        />
                        <span v-html="tag.help" />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section>
                      <q-item-label class="text-grey-9">
                        Include in shortcuts
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section>
                      <q-item-label class="text-grey-9">
                        Include in context menu
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
            </template>
          </q-list>
        </div>
      </transition>
      <q-menu
        touch-position
        context-menu
        transition-show="scale"
        transition-hide="scale"
      >
        <q-list dense separator>
          <template v-for="(tag, idx) in teiTags" :key="idx">
            <q-item clickable>
              <q-item-section>
                <q-item-label>{{ tag.name }}</q-item-label>
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-menu>
    </q-tab-panel>
    <q-tab-panel
      name="preview"
      class="render-panel"
      :style="`height: ${editorHeight}px`"
    >
      <TeiRenderer :text="currentFolioData.editorSession.getValue()" />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script>
import { filter as rFilter, isEmpty, prop, sortBy } from "ramda";
import {
  computed,
  defineComponent,
  inject,
  markRaw,
  nextTick,
  onMounted,
  onBeforeUnmount,
  ref,
  watch,
} from "vue";
import { requests } from "@/api";
import { useAPI, useEventHandling, useStores } from "@/use";
import { TeiRenderer } from "@/components";
import ace from "ace-builds";
import "ace-builds/src-noconflict/mode-xml";
import "ace-builds/src-noconflict/theme-chrome";
import { teiTags } from "./teiTags.js";

export default defineComponent({
  name: "TeiEditor",
  components: {
    TeiRenderer,
  },
  setup(_, context) {
    const { currentFolioData, sourceEditor, view } = useStores();
    const { apiInterface } = useAPI();
    const { status, data, fetchAPI } = apiInterface();
    const { notifier } = useEventHandling();
    const { editorHeight, editorWidth } = inject("editorDimensions");
    const disabled = computed(() => {
      return isEmpty(currentFolioData.value.transcription);
    });
    const tagFilter = ref("");
    var editor = null;

    /* eslint-disable */
    const teiTagsFiltered = computed(() =>
      isEmpty(tagFilter.value)
        ? sortBy(prop("name"), teiTags)
        : rFilter(
            (tag) =>
              tag.name.toLowerCase().includes(tagFilter.value.toLowerCase()),
            // tag.help.toLowerCase().includes(tagFilter.value.toLowerCase())
            // tag.tagName.toLowerCase().includes(tagFilter.value.toLowerCase())
            sortBy(prop("name"), teiTags),
          ),
    );
    /* eslint-enable */

    const checkVersion = async () => {
      await fetchAPI(
        requests.transcriptions.checkVersion(
          currentFolioData.value.transcriptionId,
          currentFolioData.value.transcriptionVersion,
        ),
      );
      if (status.value !== 200) {
        if (status.value === 205) {
          console.log(data.value);
          currentFolioData.value.transcriptionVersion =
            data.value.transcriptionVersion;
          currentFolioData.value.transcriptionAuthor =
            data.value.transcriptionAuthor;
          currentFolioData.value.transcriptionText =
            data.value.transcriptionText;
          return true;
        } else {
          notifier.transcriptions.versionCheckFailed(data.value.error);
          return false;
        }
      } else {
        return true;
      }
    };

    const updateStoreText = () => {
      return new Promise((resolve) => {
        currentFolioData.value.tei = editor.getValue();
        resolve();
      });
    };

    const onTabSwitch = (value) => {
      if (value === "preview") currentFolioData.value.tei = editor.getValue();
    };

    const loadSession = () => {
      return new Promise((resolve) => {
        checkVersion().then((result) => {
          if (result) {
            editor.setSession(currentFolioData.value.editorSession);
            resolve();
          } else {
            console.log("STALE TRANSCRIPTION!");
          }
        });
      });
    };

    const createSession = () => {
      return new Promise((resolve) => {
        currentFolioData.value.editorSession = ace.createEditSession(
          currentFolioData.value.tei,
        );
        loadSession().then(() => {
          editor.session.once(
            "change",
            () => (currentFolioData.value.hasChanges = true),
          );
          editor.session.setOptions({
            mode: "ace/mode/xml",
            useWorker: false,
            wrap: sourceEditor.value.softWrap,
          });
          resolve();
        });
      });
    };

    const insertTag = (type, tag, attributes) => {
      let tagAtt = [];
      let spAtt = {};

      if (attributes) {
        attributes = attributes.includes("-")
          ? attributes.split("-")
          : [attributes];

        attributes.forEach((attribute) => {
          let att = attribute.split("|");
          if (att.length === 2) {
            tagAtt.push([att[0], att[1]]);
          } else {
            let att_value;
            // if (att[1] === "text") {
            //   att_value = $("#"+att[2]).val();
            //   $("#"+att[2]).val("");
            // }
            // if (att[1] === "choice") {
            //   att_value = $("#"+att[2]).find("option:selected").text();
            //   $("#"+att[2])[0].selectedIndex = 0;
            // }

            if (tag === "note" || tag === "seg") {
              spAtt[att[0]] = att_value;
            } else {
              tagAtt.push([att[0], att_value]);
            }
          }
        });
      }

      if (tag === "seg") {
        tagAtt.push(["target", spAtt["target"]]);
        tagAtt.push(["rend", spAtt["rend"]]);
      }

      if (tag === "note") {
        if (spAtt["type"] === "renvoi") {
          /* eslint-disable */
          const noteRef = `<ref target="${spAtt["target"]}"/>`;
          const noteOutput = `\n\n<note xml:id="${spAtt["target"]}">${spAtt["text"]}</note>`;
          /* eslint-enable */
          editor.session.insert(editor.getCursorPosition(), noteRef);
          editor.session.insert(
            {
              row: editor.session.getLength(),
              column: 0,
            },
            noteOutput,
          );
        } else {
          /* eslint-disable */
          const tagOutput = `<note type="${spAtt["type"]}">${spAtt["text"]}</note>`;
          /* eslint-enable */
          editor.session.insert(editor.getCursorPosition(), tagOutput);
        }
      } else {
        let tagOutput = "<" + tag;

        if (tagAtt.length !== 0) {
          tagAtt.forEach((attribute) => {
            if (attribute[1] !== "" && attribute[1] !== "Join") {
              tagOutput += " " + attribute[0] + '="' + attribute[1] + '"'; // eslint-disable-line
            }
          });
        }

        if (type === "w") {
          const range = editor.selection.getRange();
          tagOutput += ">" + editor.getSelectedText() + "</" + tag + ">";
          editor.session.replace(range, tagOutput);
        } else {
          tagOutput += "/>";
          editor.session.insert(editor.getCursorPosition(), tagOutput);
        }

        if (tag === "seg") {
          /* eslint-disable */
          const noteOutput = `\n\n<note type="brace" xml:id="${spAtt["target"]}">${spAtt["text"]}</note>`;
          /* eslint-enable */
          editor.session.insert(
            {
              row: editor.session.getLength(),
              column: 0,
            },
            noteOutput,
          );
        }
      }
    };

    onMounted(async () => {
      // ace.config.set("basePath", "ace-builds/");
      view.value.editorTab = "write";
      await nextTick();
      editor = markRaw(
        ace.edit("ace-editor", {
          placeholder: "Start transcription",
          mode: "ace/mode/xml",
          theme: `ace/theme/${sourceEditor.value.theme.toLowerCase()}`,
          useWorker: false,
          readOnly: false,
          mergeUndoDeltas: true,
          highlightActiveLine: true,
          highlightSelectedWord: sourceEditor.value.highlightWord,
          highlightGutterLine: true,
          showInvisibles: sourceEditor.value.showInvisibles,
          showPrintMargin: false,
          showFoldWidgets: true,
          showLineNumbers: sourceEditor.value.showLineNumbers,
          showGutter: sourceEditor.value.showGutter,
          displayIndentGuides: sourceEditor.value.showGuides,
          fontSize: sourceEditor.value.fontSize,
          wrap: sourceEditor.value.softWrap,
          foldStyle: "markbegin",
          indentedSoftWrap: true,
          fixedWidthGutter: true,
          scrollPastEnd: false,
        }),
      );
      // createSession();
    });

    onBeforeUnmount(() => {
      var b;
      (b = editor) === null || b === void 0 ? void 0 : b.destroy();
    });

    watch([editorHeight, editorWidth], async () => {
      await nextTick();
      editor.resize();
    });

    watch(
      () => view.value.editorTab,
      () => {
        if (view.value.editorTab === "preview") updateStoreText();
      },
    );

    context.expose({
      updateStoreText,
      createSession,
      loadSession,
    });

    return {
      currentFolioData,
      disabled,
      editor,
      editorHeight,
      editorWidth,
      tagFilter,
      teiTags,
      teiTagsFiltered,
      onTabSwitch,
      view,
      insertTag,
    };
  },
});
</script>

<style lang="scss">
.ace_editor {
  white-space: pre-line;
  line-height: 1.3;
  font-family: "Menlo", "Consolas", monospace;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: transparent !important;
}
.ace_gutter {
  background: none !important;
}
.editor-panel {
  padding: 0;
  background: linear-gradient(120deg, #fefefe, #efefef) no-repeat 0px/40px 100%;
}
.tag-menu {
  overflow: scroll;
  border-left: 1px solid #d1d1d1;
  margin-left: 8px;
}
.tag-menu .q-btn-group {
  width: 100%;
  border-radius: 0;
  border-bottom: 1px solid #d1d1d1;
}
.tag-menu .q-btn-group:last-of-type {
  border-bottom: none;
}
.tag-menu-popup {
  max-width: 200px;
}
.tag-search-box .q-field__control {
  font-size: 13px;
  height: 30px;
  padding: 0px 0px 0px 5px !important;
  border-bottom: 1px solid #d1d1d1;
}
.tag-search-box .q-field__marginal,
.tag-search-box .q-field__native {
  height: 28px;
  padding: 6px 10px;
}
</style>
