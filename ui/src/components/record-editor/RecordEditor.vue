<template>
  <q-layout :style="`height: ${compositeHeight + 2}px`" view="lhh lpr lff" container>
    <q-drawer
      v-model="drawer"
      :mini="view.pageDrawerMini"
      :mini-width="parseInt(0)"
      :width="parseInt(141)"
      class="page-selector-drawer q-mini-drawer-hide"
      side="left"
    >
      <div v-if="pageChooser" :style="`height: ${compositeHeight}px`" class="page-container">
        <q-table
          :columns="columns"
          :pagination="pagination"
          :rows="view.pages"
          card-container-class="q-pa-none"
          class="sticky-header q-mini-drawer-hide"
          no-data-label="No folios found."
          row-key="id"
          grid
          hide-bottom
        >
          <template #item="props">
            <q-card
              @click="changePage(props.row.ref)"
              :class="
                props.row.ref === view.currentPageRef
                  ? 'grid-card text-weight-medium current-page'
                  : 'grid-card text-weight-medium cursor-pointer'
              "
              bordered
            >
              <q-img
                :src="props.row.thumbnailUrl"
                fit="cover"
                height="135px"
                width="108px"
                no-native-menu
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
          :class="orientationClass"
          :horizontal="view.splitterHorizontal"
          :limits="view.splitterLimits"
          separator-class="splitter-separator"
          unit="px"
          emit-immediately
        >
          <template #before>
            <IiifViewer
              @change-page="changePage"
              @toggle-drawer="toggleMini"
              @toggle-splitter="toggleSplitter"
            />
          </template>

          <template #separator>
            <q-btn
              :class="{ 'drag-button-h': view.splitterHorizontal }"
              class="splitter-separator-button strong-focus"
              icon="drag_indicator"
              icon-right="drag_indicator"
              size="xs"
              unelevated
            />
          </template>

          <template #after>
            <div v-if="editOn" class="editor-box">
              <TeiEditor v-if="editorStore.ready" ref="editor" />
              <AdaptiveSpinner v-else class="q-ma-auto" position="absolute" type="bars" />
            </div>
            <div v-else :style="`height: ${compositeHeight}px`" class="render-panel">
              <TeiRenderer :text="currentPageData.tei" />
            </div>
          </template>
        </q-splitter>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { useQuasar } from "quasar";
import { computed, defineComponent, inject, onMounted, provide, ref } from "vue";

import { AdaptiveSpinner, CustomDialog, IiifViewer, TeiRenderer } from "@/components";
import { useEventHandling, useStores } from "@/use";
import { nully } from "@/utils";

import TeiEditor from "./TeiEditor.vue";

export default defineComponent({
  name: "RecordEditor",
  components: {
    AdaptiveSpinner,
    IiifViewer,
    TeiEditor,
    TeiRenderer,
  },
  setup() {
    const $q = useQuasar();
    const {
      currentPageData,
      editOn,
      contentHeight,
      contentWidth,
      pageCount,
      views,
      view,
      showInfoArea,
      editorStore,
    } = useStores();
    const { eventBus } = useEventHandling();
    const columns = inject("pageColumns");
    const pages = view.pages;
    const pagination = ref({ rowsPerPage: 0 });

    // const getPages = () => {
    //   pages.forEach((page, idx) => {
    //     page.ref = idx;
    //     page.editorTab = "preview";
    //     page.dbTei = page.transcription?.transcription;
    //     page.tei = page.transcription?.transcription;
    //     page.viewerZoom = 0;
    //   });
    //   return pages;
    // };

    // views.mergeValues(views, {
    //   pages: getPages(),
    //   currentPageRef: 0,
    //   pageDrawerMini: true,
    //   showTagMenu: false,
    //   splitterHorizontal: true,
    //   editorSplitter: 0,
    //   lastSplitter: 0,
    //   editOn: false,
    // });

    const drawer = ref(pageCount.value > 1);
    const pageChooser = computed(() => pageCount.value > 1);
    const editor = ref(null);

    const infoAreaHeight = computed(() => (showInfoArea.value ? 75 : 0));
    const pageDrawerWidth = computed(() => (view.value.pageDrawerMini ? 0 : 141));
    const orientationClass = computed(() =>
      view.value.splitterHorizontal ? "editor-horizontal" : "editor-vertical",
    );

    const compositeHeight = computed(() => {
      const tabs = 37 + 8; // tab-bar + padding;
      return Math.round(contentHeight.value - infoAreaHeight.value - tabs);
    });

    if (!view.value.editorSplitter) {
      view.value.editorSplitter = Math.round(compositeHeight.value / 2);
    }

    const editorHeight = computed(() => {
      const toolbar = 40;
      const splitter = 7;
      return view.value.splitterHorizontal
        ? Math.round(compositeHeight.value - view.value.editorSplitter - toolbar - splitter)
        : compositeHeight.value - toolbar;
    });

    const editorWidth = computed(() =>
      view.value.splitterHorizontal
        ? Math.round(contentWidth.value)
        : Math.round(contentWidth.value - view.value.editorSplitter),
    );

    const viewerHeight = computed(() =>
      view.value.splitterHorizontal
        ? compositeHeight.value - editorHeight.value
        : compositeHeight.value,
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
      if (view.value.editOn && views.hasChanges) {
        $q.dialog({
          component: CustomDialog,
          componentProps: {
            isPersistent: true,
            title: "Save changes",
            closeIcon: false,
            message:
              "There is unsaved data in the current record. Do you wish to save your changes?",
            icon: "exit_to_app",
            okayButtonLabel: "Save",
          },
        }).onOk(() => {
          console.log("Save changes");
          eventBus.emit("destroyEditor");
          view.value.editOn = !view.value.editOn;
        });
      } else {
        view.value.editOn = !view.value.editOn;
      }
    };

    const changePage = (para) => {
      let targetPage = null;
      if (Number.isInteger(para)) targetPage = para;
      if (para === "first") targetPage = 0;
      if (para === "last") targetPage = pages.length - 1;
      if (para === "prev") targetPage = view.value.currentPageRef - 1;
      if (para === "next") targetPage = view.value.currentPageRef + 1;
      view.value.currentPageRef = targetPage;
    };

    eventBus.on("changePage", (page) => changePage(page));
    eventBus.on("toggleEditor", toggleEditor);

    provide("editorDimensions", { editorHeight, editorWidth });
    provide("viewerDimensions", { viewerHeight, viewerWidth });

    onMounted(async () => {
      if (!editorStore.ready) {
        editorStore.initialize().then(() => {
          // TODO: temp workaround - this should be set by the UI
          editorStore.currentSetId = editorStore.sets()[0].id;
        });
      }
    });

    return {
      nully,
      changePage,
      currentPageData,
      editOn,
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
      splitterLimits,
      toggleEditor,
      toggleMini,
      toggleSplitter,
      view,
      orientationClass,
      editorStore,
    };
  },
});
</script>

<style lang="scss" scoped>
/* Splitter */
.q-layout-container,
.q-splitter {
  transition: height 0.2s ease-in-out;
}
.q-splitter {
  border: 1px solid #d1d1d1;
  border-radius: 4px;
}
/* Splitter - IIIF Viewer */
:deep(.q-splitter__before) {
  background-color: rgb(71, 71, 71);
}
:deep(.editor-horizontal .q-splitter__before) {
  border-top-right-radius: 3px;
  border-top-left-radius: 3px;
}
:deep(.editor-vertical .q-splitter__before) {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}
:deep(.q-splitter__panel.q-splitter__before) {
  display: flex;
}
:deep(.q-splitter--horizontal .q-splitter__panel.q-splitter__before) {
  flex-direction: column;
}
/* Splitter - Editor */
:deep(.q-splitter__after) {
  border-bottom-right-radius: 3px;
}
:deep(.q-splitter--horizontal .q-splitter__after) {
  border-bottom-left-radius: 3px;
}
:deep(.q-splitter--vertical .q-splitter__after) {
  border-bottom-left-radius: 0;
  border-top-right-radius: 3px;
}
:deep(.editor-box),
:deep(.q-splitter__panel.q-splitter__after) {
  overflow: hidden;
}
/* Splitter - TEI renderer */
.render-panel {
  background: #ffffff;
  padding: 16px;
  overflow: scroll;
}
/* Splitter separator */
:deep(.splitter-separator.q-splitter__separator) {
  background-color: #c5cae9;
  border: 1px solid #5c6bc0;
}
:deep(.q-splitter--horizontal > .splitter-separator.q-splitter__separator) {
  height: 7px;
  margin-right: -1px;
  margin-left: -1px;
  border-left-color: transparent;
  border-right-color: transparent;
  box-shadow:
    0px 1px 0px 0px #dee2fc inset,
    0px -1px 0px 0px #aeb7e7 inset;
}
:deep(.q-splitter--vertical > .splitter-separator.q-splitter__separator) {
  width: 7px;
  margin-top: -1px;
  margin-bottom: -1px;
  border-top-color: transparent;
  border-top-color: transparent;
  box-shadow:
    1px 0px 0px 0px #dee2fc inset,
    -1px 0px 0px 0px #aeb7e7 inset;
}
/* Splitter separator button */
:deep(.splitter-separator-button) {
  height: 60px;
  padding: 0;
  background-color: #c5cae9;
  color: #5c6bc0;
  border: 1px solid #5c6bc0;
}
:deep(.drag-button-h) {
  transform: rotate(90deg) translate(-30px, -10px);
}
:deep(.q-splitter--horizontal .splitter-separator-button) {
  box-shadow:
    1px 0px 0px 0px #dee2fc inset,
    -1px 0px 0px 0px #aeb7e7 inset;
}
:deep(.q-splitter--vertical .splitter-separator-button) {
  box-shadow:
    0px 1px 0px 0px #dee2fc inset,
    0px -1px 0px 0px #aeb7e7 inset;
}
:deep(.splitter-separator-button i) {
  font-size: 1.3em !important;
}
:deep(.splitter-separator-button i:first-of-type) {
  bottom: -0.25em;
}
:deep(.splitter-separator-button span.q-btn__content) {
  flex-direction: column;
}
/* Page selector */
:deep(.page-selector-drawer) {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-top: 1px solid #d1d1d1;
  border-bottom: 1px solid #d1d1d1;
  border-right: 1px solid #d1d1d1;
}
.page-container {
  overflow-y: scroll;
}
/* Page selector card */
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
</style>
