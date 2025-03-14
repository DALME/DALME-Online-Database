<template>
  <q-layout view="lhh lpr lff" container :style="`height: ${compositeHeight + 4}px`">
    <q-drawer
      v-model="drawer"
      side="left"
      :mini="view.pageDrawerMini"
      class="detail-drawer-left q-mini-drawer-hide"
      :width="parseInt(141)"
      :mini-width="parseInt(0)"
    >
      <div v-if="pageChooser" class="page-container" :style="`height: ${compositeHeight}px`">
        <q-table
          grid
          hide-bottom
          card-container-class="q-pa-none"
          :rows="view.pages"
          :columns="columns"
          no-data-label="No folios found."
          row-key="id"
          class="sticky-header q-mini-drawer-hide"
          :pagination="pagination"
        >
          <template v-slot:item="props">
            <q-card
              bordered
              :class="
                props.row.ref === view.currentPageRef
                  ? 'grid-card text-weight-medium current-page'
                  : 'grid-card text-weight-medium cursor-pointer'
              "
              @click="changePage(props.row.ref)"
            >
              <q-img
                no-native-menu
                width="108px"
                height="135px"
                fit="cover"
                :src="props.row.thumbnailUrl"
              />
              <q-card-section class="q-px-sm q-py-xs text-detail">
                Folio {{ props.row.name }}
              </q-card-section>
            </q-card>
          </template>
        </q-table>
      </div>
    </q-drawer>

    <q-page-container>
      <q-page :class="!view.pageDrawerMini ? 'q-pl-sm q-pr-none' : 'q-pa-none'">
        <q-splitter
          v-model="view.editorSplitter"
          unit="px"
          :horizontal="view.splitterHorizontal"
          separator-class="splitter-separator"
          :limits="view.splitterLimits"
          emit-immediately
          :class="orientationClass"
        >
          <template v-slot:before>
            <IiifViewer
              @changePage="changePage"
              @toggleSplitter="toggleSplitter"
              @toggleDrawer="toggleMini"
            />
          </template>

          <template v-slot:separator>
            <q-btn
              unelevated
              size="xs"
              icon="drag_indicator"
              icon-right="drag_indicator"
              class="splitter-separator-button strong-focus"
              :class="{ 'drag-button-h': view.splitterHorizontal }"
            />
          </template>

          <template v-slot:after>
            <div v-show="currentPageData.editOn" class="editor-box">
              <TeiEditor v-if="settings.teiReady" ref="editor" />
              <AdaptiveSpinner type="bars" position="absolute" v-else />
            </div>
            <div
              v-show="!currentPageData.editOn"
              class="render-panel"
              :style="`height: ${compositeHeight}px`"
            >
              <TeiRenderer :text="currentPageData.tei" />
            </div>
          </template>
        </q-splitter>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { computed, defineComponent, inject, onMounted, provide, ref } from "vue";
import { useEventHandling, useStores } from "@/use";
import { AdaptiveSpinner, IiifViewer, TeiRenderer } from "@/components";
import TeiEditor from "./TeiEditor.vue";
import { nully } from "@/utils";

export default defineComponent({
  name: "RecordEditor",
  components: {
    AdaptiveSpinner,
    IiifViewer,
    TeiEditor,
    TeiRenderer,
  },
  setup() {
    const { currentPageData, contentHeight, contentWidth, pageCount, settings, views, view } =
      useStores();
    const { eventBus } = useEventHandling();
    const columns = inject("columns");
    const pages = inject("pages");
    const showInfoArea = inject("showInfoArea");
    const pagination = ref({ rowsPerPage: 0 });

    const getPages = () => {
      pages.forEach((page, idx) => {
        page.ref = idx;
        page.editorTab = "write";
        page.editOn = false;
        page.tei = page.transcription?.transcription;
        page.hasChanges = false;
        page.viewerZoom = 0;
      });
      return pages;
    };

    views.mergeValues(views, {
      pages: getPages(),
      currentPageRef: 0,
      pageDrawerMini: true,
      showTagMenu: false,
      splitterHorizontal: true,
      editorSplitter: 0,
      lastSplitter: 0,
      editorTab: "write",
    });

    const drawer = ref(pageCount.value > 1);
    const pageChooser = computed(() => pageCount.value > 1);
    const editor = ref(null);

    const infoAreaHeight = computed(() => (showInfoArea.value ? 75 : 0));
    const pageDrawerWidth = computed(() => (view.value.pageDrawerMini ? 0 : 141));
    const orientationClass = computed(() =>
      view.value.splitterHorizontal ? "editor-horizontal" : "editor-vertical",
    );

    const compositeHeight = computed(() => {
      const tabs = 37 + 16; // tab-bar + margin;
      return Math.round(contentHeight.value - infoAreaHeight.value - tabs);
    });

    if (!view.value.editorSplitter) {
      view.value.editorSplitter = Math.round(compositeHeight.value / 2);
    }

    const editorHeight = computed(() => {
      const editorToolbar = 40;
      return view.value.splitterHorizontal
        ? Math.round(compositeHeight.value - editorToolbar - view.value.editorSplitter)
        : compositeHeight.value - editorToolbar;
    });

    const editorWidth = computed(() =>
      view.value.splitterHorizontal
        ? Math.round(contentWidth.value)
        : Math.round(contentWidth.value - view.value.editorSplitter),
    );

    const viewerHeight = computed(
      () =>
        view.value.splitterHorizontal
          ? compositeHeight.value - editorHeight.value
          : compositeHeight.value + 4, // border adjustment
    );

    const viewerWidth = computed(() =>
      view.value.splitterHorizontal
        ? contentWidth.value - pageDrawerWidth.value
        : view.value.editorSplitter,
    );

    const separatorHeight = computed(() =>
      view.value.splitterHorizontal ? 4 : compositeHeight.value,
    );

    const separatorWidth = computed(() => (view.value.splitterHorizontal ? viewerWidth.value : 4));

    const splitterLimits = computed(() =>
      view.value.splitterHorizontal
        ? [40, compositeHeight.value - 10]
        : [70, contentWidth.value - 10],
    );

    const currentSplitterPercentage = computed(() => {
      let total = view.value.splitterHorizontal ? compositeHeight.value : contentWidth.value;
      return Math.round((view.value.editorSplitter * 100) / total);
    });

    const nextSplitterPixels = computed(() => {
      let total = view.value.splitterHorizontal ? contentWidth.value : compositeHeight.value;
      return view.value.lastSplitter ? Math.round((view.value.lastSplitter * total) / 100) : 0;
    });

    const toggleSplitter = () => {
      let targetSplit = nextSplitterPixels.value
        ? nextSplitterPixels.value
        : view.value.splitterHorizontal
          ? Math.round(contentWidth.value / 2)
          : Math.round(compositeHeight.value / 2);
      view.value.lastSplitter = currentSplitterPercentage.value;
      view.value.splitterHorizontal = !view.value.splitterHorizontal;
      view.value.editorSplitter = targetSplit;
    };

    const toggleMini = () => {
      view.value.pageDrawerMini = !view.value.pageDrawerMini;
      if (!view.value.splitterHorizontal) {
        view.value.editorSplitter = view.value.pageDrawerMini
          ? view.value.editorSplitter + 141
          : view.value.editorSplitter - 141;
      }
    };

    const toggleEditor = () => {
      return new Promise((resolve) => {
        if (!currentPageData.value.editOn) {
          editor.value.createSession().then(() => {
            currentPageData.value.editOn = true;
          });
        } else {
          currentPageData.value.editOn = false;
        }
        resolve();
      });
    };

    const changePage = (para) => {
      let targetPage = null;
      if (Number.isInteger(para)) targetPage = para;
      if (para === "first") targetPage = 0;
      if (para === "last") targetPage = pages.length - 1;
      if (para === "prev") targetPage = view.value.currentPageRef - 1;
      if (para === "next") targetPage = view.value.currentPageRef + 1;

      // if (currentPageData.value.editOn) await editor.value.updateStoreText();
      view.value.currentPageRef = targetPage;
      // await nextTick();
      // if (currentPageData.value.editOn) await editor.value.loadSession();
    };

    eventBus.on("changePage", (page) => changePage(page));
    eventBus.on("toggleEditor", toggleEditor);

    provide("editorDimensions", { editorHeight, editorWidth });
    provide("viewerDimensions", { viewerHeight, viewerWidth });

    onMounted(async () => {
      if (!settings.teiReady) {
        const data = await settings.fetchTeiElements();
        if (data) {
          settings.teiElementSetData = data.sets;
          settings.teiElementData = data.elements;
          settings.teiTagData = data.tags;
          // temp workaround - this should be set by the UI
          settings.currentSetId = data.sets[0].id;
        }
      }
    });

    return {
      nully,
      changePage,
      currentPageData,
      columns,
      drawer,
      editor,
      contentHeight,
      contentWidth,
      compositeHeight,
      editorHeight,
      editorWidth,
      pageChooser,
      pages,
      pagination,
      separatorHeight,
      separatorWidth,
      settings,
      splitterLimits,
      toggleEditor,
      toggleMini,
      toggleSplitter,
      view,
      orientationClass,
    };
  },
});
</script>

<style lang="scss">
.drag-button-h {
  transform: rotate(90deg) translate(-30px, -10px);
}
.splitter-separator.q-splitter__separator {
  background-color: #c5cae9;
  border: 1px solid #5c6bc0;
}
.q-splitter--horizontal > .splitter-separator.q-splitter__separator {
  height: 7px;
  box-shadow:
    0px 1px 0px 0px #dee2fc inset,
    0px -1px 0px 0px #aeb7e7 inset;
}
.q-splitter--vertical > .splitter-separator.q-splitter__separator {
  width: 7px;
  box-shadow:
    1px 0px 0px 0px #dee2fc inset,
    -1px 0px 0px 0px #aeb7e7 inset;
}
.splitter-separator-button {
  height: 60px;
  padding: 0;
  background-color: #c5cae9;
  color: #5c6bc0;
  border: 1px solid #5c6bc0;
}
.q-splitter--horizontal .splitter-separator-button {
  box-shadow:
    1px 0px 0px 0px #dee2fc inset,
    -1px 0px 0px 0px #aeb7e7 inset;
}
.q-splitter--vertical .splitter-separator-button {
  box-shadow:
    0px 1px 0px 0px #dee2fc inset,
    0px -1px 0px 0px #aeb7e7 inset;
}
.splitter-separator-button i {
  font-size: 1.3em !important;
}
.splitter-separator-button i:first-of-type {
  bottom: -0.25em;
}
.splitter-separator-button span.q-btn__content {
  flex-direction: column;
}
.grid-card {
  width: 110px;
  margin-top: 12px;
  margin-left: 12px;
  border-color: #d1d1d1;
  color: #757575;
}
.grid-card:last-of-type {
  margin-bottom: 12px;
}
.grid-card .q-img__container {
  border-bottom: 1px solid transparent;
}
.grid-card.current-page {
  background: #c5cae9;
  border-color: #3949ab;
  color: #3949ab;
}
.grid-card.current-page .q-img__container {
  border-bottom: 1px solid #3949ab;
}
.q-splitter__after {
  border-bottom: 1px solid #d1d1d1;
  border-right: 1px solid #d1d1d1;
  border-bottom-right-radius: 4px;
}
.q-splitter--horizontal .q-splitter__after {
  border-left: 1px solid #d1d1d1;
  border-bottom-left-radius: 4px;
}
.q-splitter--vertical .q-splitter__after {
  border-top: 1px solid #d1d1d1;
  border-bottom-left-radius: 0;
  border-top-right-radius: 4px;
}
.editor-box,
.q-splitter__panel.q-splitter__after {
  overflow: hidden;
}
.q-splitter__panel.q-splitter__before {
  display: flex;
}
.q-splitter--horizontal .q-splitter__panel.q-splitter__before {
  flex-direction: column;
}
.render-panel {
  background: #ffffff;
  padding: 16px;
  overflow: scroll;
}
.page-container {
  overflow-y: scroll;
}
.detail-drawer-left {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-top: 1px solid #d1d1d1;
  border-bottom: 1px solid #d1d1d1;
  border-right: 1px solid #d1d1d1;
}
.q-layout-container,
.q-splitter {
  transition: height 0.2s ease-in-out;
}
.q-splitter__before {
  background-color: rgb(71, 71, 71);
}
.editor-horizontal .q-splitter__before {
  border-top-right-radius: 4px;
  border-top-left-radius: 4px;
}
.editor-vertical .q-splitter__before {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
</style>
