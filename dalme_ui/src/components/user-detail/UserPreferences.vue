<template>
  <q-card flat bordered class="detail-card full-width">
    <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
      <q-item-section side class="q-pr-sm">
        <q-icon name="settings" color="indigo-5" size="xs" />
      </q-item-section>
      <q-item-section>
        <q-item-label class="text-subtitle2">Preferences</q-item-label>
      </q-item-section>
    </q-item>
    <q-separator class="bg-indigo-3" />
    <q-card-section class="q-pa-none">
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="left"
        no-caps
        narrow-indicator
      >
        <q-tab name="ui" label="User Interface" />
        <q-tab name="editor" label="Source Editor" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="ui">
          <q-list>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="tooltipsOn"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Show Tooltips</q-item-label>
                <q-item-label caption>
                  Hover over interface elements to show their function.
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="sidebarCollapsed"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Use Compact Sidebar</q-item-label>
                <q-item-label caption>
                  Sidebar collapses to occupy minimal space and expands as an overlay when hovering.
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>
        <q-tab-panel name="editor">
          <q-list>
            <q-item>
              <q-item-section avatar>
                <q-select dense v-model="theme" :options="themeList">
                  <template v-slot:option="scope">
                    <q-item dense v-bind="scope.itemProps">
                      <q-item-section>
                        <q-item-label>{{ scope.opt.label }}</q-item-label>
                        <q-item-label caption>
                          {{ scope.opt.type }}
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>
              </q-item-section>
              <q-item-section>
                <q-item-label>Theme</q-item-label>
                <q-item-label caption> Change text and syntax highlighting colours. </q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section avatar>
                <q-input
                  v-model.number="fontSize"
                  type="number"
                  filled
                  style="width: 80px"
                  suffix="px"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Font Size</q-item-label>
                <q-item-label caption>
                  Set the editor's font size in pixels (default is 14).
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="highlightWord"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Highlight Word</q-item-label>
                <q-item-label caption>
                  When a word is selected the editor highlights all other occurrences of the same
                  word in the text.
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="showGuides"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Show Guides</q-item-label>
                <q-item-label caption>??</q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="showGutter"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Show Gutter</q-item-label>
                <q-item-label caption>
                  Show gutter on left side of the editor's window.
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="showInvisibles"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Show Invisibles</q-item-label>
                <q-item-label caption>
                  Show invisible characters such as spaces, tabs, and line breaks.
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="showLineNumbers"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Show Line Numbers</q-item-label>
                <q-item-label caption>
                  Show line numbers in the gutter (Show Gutter must also be on). When Soft Wrap is
                  active, wrapped lines show without numbers.
                </q-item-label>
              </q-item-section>
            </q-item>
            <q-item tag="label" v-ripple>
              <q-item-section avatar>
                <q-toggle
                  checked-icon="visibility"
                  unchecked-icon="visibility_off"
                  color="green"
                  v-model="softWrap"
                  size="lg"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Soft Wrap Text</q-item-label>
                <q-item-label caption>
                  Visually wrap long lines of text if they exceed the width of the editor's window.
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-tab-panel>
      </q-tab-panels>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useStores } from "@/use";

const themeList = [
  { label: "Chrome", value: "ace/theme/chrome", type: "Light theme" },
  { label: "Clouds", value: "ace/theme/clouds", type: "Light theme" },
  { label: "XCode", value: "ace/theme/xcode", type: "Light theme" },
  { label: "Kuroir", value: "ace/theme/kuroir", type: "Light theme" },
  { label: "SQL Server", value: "ace/theme/sqlserver", type: "Light theme" },
  {
    label: "Clouds Midnight",
    value: "ace/theme/clouds_midnight",
    type: "Dark theme",
  },
  { label: "Cobalt", value: "ace/theme/cobalt", type: "Dark theme" },
  {
    label: "Idle Fingers",
    value: "ace/theme/idle_fingers",
    type: "Dark theme",
  },
  { label: "Terminal", value: "ace/theme/terminal", type: "Dark theme" },
  {
    label: "Tomorrow Night Blue",
    value: "ace/theme/tomorrow_night_blue",
    type: "Dark theme",
  },
];

export default defineComponent({
  name: "UserPreferences",
  setup() {
    // const { apiInterface } = useAPI();
    // const { loading, success, data, fetchAPI } = apiInterface();
    const { general, sourceEditor } = useStores();
    const tab = ref("ui");
    const tooltipsOn = ref(general.tooltipsOn);
    const sidebarCollapsed = ref(general.sidebarCollapsed);
    const theme = ref(sourceEditor.value.theme);
    const fontSize = ref(sourceEditor.value.fontSize);
    const highlightWord = ref(sourceEditor.value.highlightWord);
    const showGuides = ref(sourceEditor.value.showGuides); // displayIndentGuides??
    const showGutter = ref(sourceEditor.value.showGutter);
    const showInvisibles = ref(sourceEditor.value.showInvisibles);
    const showLineNumbers = ref(sourceEditor.value.showLineNumbers);
    const softWrap = ref(sourceEditor.value.softWrap);

    // For certain resources: e.g. records
    // show own / show team's / show all non-private

    // for lists:
    // remember column visibility Preferences
    // remember sort order
    // remember max rows show

    // homepage:
    // choose tiles to show

    // other options: https://github.com/ajaxorg/ace/wiki/Configuring-Ace
    // selectionStyle: "line"|"text"
    // highlightActiveLine: true|false
    // cursorStyle: "ace"|"slim"|"smooth"|"wide"
    // highlightGutterLine: boolean
    // showFoldWidgets: boolean (defaults to true)

    const onSubmit = () => {
      console.log("submit");
    };

    return {
      onSubmit,
      tab,
      tooltipsOn,
      sidebarCollapsed,
      theme,
      themeList,
      fontSize,
      highlightWord,
      showGuides,
      showGutter,
      showInvisibles,
      showLineNumbers,
      softWrap,
    };
  },
});
</script>
