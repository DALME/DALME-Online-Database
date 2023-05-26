<template>
  <q-layout
    view="lhh lpr lff"
    container
    :style="`height: ${containerHeight}px`"
  >
    <q-drawer
      v-model="drawer"
      side="left"
      :mini="view.folioDrawerMini"
      class="detail-drawer-left q-mini-drawer-hide"
      :width="parseInt(141)"
      :mini-width="parseInt(0)"
    >
      <div
        v-if="folioChooser"
        class="folio-container"
        :style="`height: ${containerHeight}px`"
      >
        <q-table
          grid
          hide-bottom
          card-container-class="q-pa-none"
          :rows="view.folios"
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
                props.row.ref === view.currentFolioRef
                  ? 'grid-card text-weight-medium current-folio'
                  : 'grid-card text-weight-medium cursor-pointer'
              "
              @click="changeFolio(props.row.ref)"
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
      <q-page :class="!view.folioDrawerMini ? 'q-pl-sm' : ''">
        <q-splitter
          v-model="view.editorSplitter"
          unit="px"
          :horizontal="view.splitterHorizontal"
          separator-class="splitter-separator"
          :limits="view.splitterLimits"
          :style="`height: ${containerHeight}px; width: ${containerWidth}px`"
        >
          <template v-slot:before>
            <IiifViewer
              @changeFolio="changeFolio"
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
            <div v-show="currentFolioData.editOn" class="editor-box">
              <TeiEditor ref="editor" />
            </div>
            <div
              v-show="!currentFolioData.editOn"
              class="render-panel"
              :style="`height: ${editorHeight}px`"
            >
              <TeiRenderer :text="currentFolioData.tei" />
            </div>
          </template>
        </q-splitter>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import {
  computed,
  defineComponent,
  inject,
  nextTick,
  provide,
  ref,
  onBeforeUnmount,
  onUnmounted,
  // watch,
} from "vue";
import { useEventHandling, useStores } from "@/use";
import { IiifViewer, TeiEditor, TeiRenderer } from "@/components";
import { notNully } from "@/utils";

export default defineComponent({
  name: "SourceEditor",
  components: {
    IiifViewer,
    TeiEditor,
    TeiRenderer,
  },
  setup() {
    const {
      currentFolioData,
      containerHeight,
      containerWidth,
      folioCount,
      ui,
      views,
      view,
    } = useStores();
    const { eventBus } = useEventHandling();
    const columns = inject("columns");
    const pages = inject("pages");
    const pagination = ref({ rowsPerPage: 0 });

    const getFolios = () => {
      pages.forEach((page, idx) => {
        page.ref = idx;
        page.editorTab = "write";
        page.editOn = false;
        page.editorSession = null;
        page.tei = page.transcriptionText;
        page.hasChanges = false;
        page.viewerZoom = 0;
      });
      return pages;
    };

    views.mergeValues({
      folios: getFolios(),
      currentFolioRef: 0,
      folioDrawerMini: true,
      showTagMenu: false,
      splitterHorizontal: true,
      editorSplitter: 0,
      lastSplitter: 0,
      editorTab: "write",
    });

    const drawer = ref(folioCount.value > 1);
    const folioChooser = computed(() => folioCount.value > 1);
    const tagMenuDrawer = computed(() => {
      return view.value.showTagMenu ? 250 : 0;
    });

    const editor = ref(null);

    if (!view.value.editorSplitter) {
      view.value.editorSplitter = Math.round(containerHeight.value / 2);
    }

    /* eslint-disable */
    const editorHeight = computed(() =>
      view.value.splitterHorizontal
        ? currentFolioData.value.editOn
          ? Math.round(containerHeight.value - view.value.editorSplitter - 60)
          : Math.round(containerHeight.value - view.value.editorSplitter - 8)
        : currentFolioData.value.editOn
        ? Math.round(containerHeight.value - 54)
        : containerHeight.value,
    );
    /* eslint-enable */
    const editorWidth = computed(() =>
      view.value.splitterHorizontal
        ? containerWidth.value - view.value.tagMenuDrawer - 2
        : Math.round(containerWidth.value - view.value.editorSplitter) -
          view.value.tagMenuDrawer -
          8,
    );

    const viewerHeight = computed(() =>
      view.value.splitterHorizontal
        ? view.value.editorSplitter
        : containerHeight.value,
    );

    const viewerWidth = computed(() =>
      view.value.splitterHorizontal
        ? containerWidth.value
        : view.value.editorSplitter,
    );

    const separatorHeight = computed(() =>
      view.value.splitterHorizontal ? 4 : viewerHeight.value,
    );

    const separatorWidth = computed(() =>
      view.value.splitterHorizontal ? viewerWidth.value : 4,
    );

    const splitterLimits = computed(() =>
      view.value.splitterHorizontal
        ? [40, containerHeight.value - 10]
        : [70, containerWidth.value - 10],
    );

    const currentSplitterPercentage = computed(() => {
      let total = view.value.splitterHorizontal
        ? containerHeight.value
        : containerWidth.value;
      return Math.round((view.value.editorSplitter * 100) / total);
    });

    const nextSplitterPixels = computed(() => {
      let total = view.value.splitterHorizontal
        ? containerWidth.value
        : containerHeight.value;
      return view.value.lastSplitter
        ? Math.round((view.value.lastSplitter * total) / 100)
        : 0;
    });

    const toggleSplitter = () => {
      let targetSplit = nextSplitterPixels.value
        ? nextSplitterPixels.value
        : view.value.splitterHorizontal //eslint-disable-line
        ? Math.round(containerWidth.value / 2) //eslint-disable-line
        : Math.round(containerHeight.value / 2); //eslint-disable-line
      view.value.lastSplitter = currentSplitterPercentage.value;
      view.value.splitterHorizontal = !view.value.splitterHorizontal;
      view.value.editorSplitter = targetSplit;
    };

    const toggleMini = () => {
      view.value.folioDrawerMini = !view.value.folioDrawerMini;
    };

    const toggleEditor = () => {
      return new Promise((resolve) => {
        if (!currentFolioData.value.editOn) {
          editor.value.createSession().then(() => {
            currentFolioData.value.editOn = true;
          });
        } else {
          console.log("save and stuff");
          currentFolioData.value.editOn = false;
        }
        resolve();
      });
    };

    const changeFolio = async (para) => {
      let targetFolio = null;
      if (Number.isInteger(para)) targetFolio = para;
      if (para === "first") targetFolio = 0;
      if (para === "last") targetFolio = pages.length - 1;
      if (para === "prev") targetFolio = view.value.currentFolioRef - 1;
      if (para === "next") targetFolio = view.value.currentFolioRef + 1;

      if (currentFolioData.value.editOn) await editor.value.updateStoreText();
      view.value.currentFolioRef = targetFolio;
      await nextTick();
      if (currentFolioData.value.editOn) await editor.value.loadSession();
    };

    eventBus.on("changeFolio", (folio) => changeFolio(folio));
    eventBus.on("toggleEditor", toggleEditor);

    provide("editorDimensions", { editorHeight, editorWidth });
    provide("viewerDimensions", { viewerHeight, viewerWidth });
    provide("folioDrawerOpen", drawer);

    onBeforeUnmount(() => {
      console.log("editor beforeUnmount");
    });
    onUnmounted(() => {
      console.log("editor unmounted");
    });

    return {
      notNully,
      changeFolio,
      currentFolioData,
      columns,
      drawer,
      editor,
      containerHeight,
      containerWidth,
      editorHeight,
      editorWidth,
      folioChooser,
      pages,
      pagination,
      separatorHeight,
      separatorWidth,
      splitterLimits,
      toggleEditor,
      toggleMini,
      toggleSplitter,
      view,
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
  box-shadow: 0px 1px 0px 0px #dee2fc inset, 0px -1px 0px 0px #aeb7e7 inset;
}
.q-splitter--vertical > .splitter-separator.q-splitter__separator {
  width: 7px;
  box-shadow: 1px 0px 0px 0px #dee2fc inset, -1px 0px 0px 0px #aeb7e7 inset;
}
.splitter-separator-button {
  height: 60px;
  padding: 0;
  background-color: #c5cae9;
  color: #5c6bc0;
  border: 1px solid #5c6bc0;
}
.q-splitter--horizontal .splitter-separator-button {
  box-shadow: 1px 0px 0px 0px #dee2fc inset, -1px 0px 0px 0px #aeb7e7 inset;
}
.q-splitter--vertical .splitter-separator-button {
  box-shadow: 0px 1px 0px 0px #dee2fc inset, 0px -1px 0px 0px #aeb7e7 inset;
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
.grid-card.current-folio {
  background: #c5cae9;
  border-color: #3949ab;
  color: #3949ab;
}
.grid-card.current-folio .q-img__container {
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
.folio-container {
  overflow-y: scroll;
}
.detail-drawer-left {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  border-top: 1px solid #d1d1d1;
  border-bottom: 1px solid #d1d1d1;
  border-right: 1px solid #d1d1d1;
  overflow: hidden !important;
}
</style>
