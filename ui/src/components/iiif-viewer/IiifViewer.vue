<template>
  <div id="viewer-container" :style="`height: ${viewerHeight}px; width: ${viewerWidth}px`">
    <div
      v-if="pageCount > 1"
      :class="`viewer-toolbar ${tbVertAlt ? 'toolbar-v' : 'toolbar-h'}`"
      :style="navPosition"
    >
      <q-btn @click="changePage('first')" :disabled="view.currentPageRef === 0" icon="first_page" />
      <q-btn
        @click="changePage('prev')"
        :disabled="view.currentPageRef === 0"
        icon="navigate_before"
      />
      <div class="viewer-current-page">{{ currentPageData.name }}</div>
      <q-btn
        @click="changePage('next')"
        :disabled="view.currentPageRef === pageCount - 1"
        icon="navigate_next"
      />
      <q-btn
        @click="changePage('last')"
        :disabled="view.currentPageRef === pageCount - 1"
        icon="last_page"
      />
    </div>
    <div
      :class="`viewer-toolbar tb-zoom ${tbHorAlt ? 'toolbar-h' : 'toolbar-v'}`"
      :style="zoomPosition"
    >
      <q-btn
        @click="zoom('in')"
        :disabled="currentPageData.viewerZoom >= maxZoomLevel"
        class="zoom-btn"
        icon="zoom_in"
      />
      <q-btn
        @click="zoom('out')"
        :disabled="currentPageData.viewerZoom <= minZoomLevel"
        class="zoom-btn"
        icon="zoom_out"
      />
      <q-btn @click="zoom('full')" icon="aspect_ratio" />
      <q-btn @click="zoom('fitV')" icon="expand" />
      <q-btn @click="zoom('fitH')">
        <q-icon class="rotate-90" name="expand" />
      </q-btn>
    </div>
    <div :style="toolPosition" class="viewer-toolbar toolbar-h">
      <q-btn
        @click="changeSplitView"
        :icon="view.splitterHorizontal ? 'o_border_vertical' : 'o_border_horizontal'"
      />
      <q-btn
        v-if="pageCount > 1"
        @click="changeDrawerMini"
        :class="view.pageDrawerMini ? '' : 'crossed-out'"
        icon="o_auto_stories"
      />
    </div>
  </div>
</template>

<script>
import OpenSeadragon from "openseadragon";
import { isEmpty } from "ramda";
import {
  computed,
  defineComponent,
  inject,
  markRaw,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from "vue";

import { useStores } from "@/use";

export default defineComponent({
  name: "IiifViewer",
  emits: ["changePage", "toggleSplitter", "toggleDrawer"],
  setup(_, context) {
    var viewer = null;
    const { viewerHeight, viewerWidth } = inject("viewerDimensions");
    const { currentPageData, pageCount, view } = useStores();

    const tbHorAlt = computed(() => view.value.splitterHorizontal && viewerHeight.value < 198);
    const tbVertAlt = computed(() => !view.value.splitterHorizontal && viewerWidth.value < 240);
    const navPosition = computed(() => {
      let top = tbVertAlt.value ? 199 : 5;
      let posHor = tbVertAlt.value ? "left" : "right";
      return `top: ${top}px; ${posHor}: 5px`;
    });
    const toolPosition = computed(() => "top: 5px; left: 5px");
    const zoomPosition = computed(() => {
      let top = tbHorAlt.value ? 5 : 42;
      let left = tbHorAlt.value ? (pageCount.value > 1 ? 71 : 41) : 5;
      return `top: ${top}px; left: ${left}px`;
    });

    const minZoomLevel = ref(0.5);
    const maxZoomLevel = ref(8);
    const defaultZoomLevel = computed(() =>
      currentPageData.value.viewerZoom ? currentPageData.value.viewerZoom : 1,
    );

    const zoom = (type) => {
      if (type === "full") console.log(currentPageData.value.ref - 1);
      if (type === "out") {
        let level = currentPageData.value.viewerZoom - 0.25;
        if (level <= minZoomLevel.value) level = minZoomLevel.value;
        viewer.viewport.zoomTo(level);
      }
      if (type === "in") {
        let level = currentPageData.value.viewerZoom + 0.25;
        if (level >= maxZoomLevel.value) level = maxZoomLevel.value;
        viewer.viewport.zoomTo(level);
      }
      if (type === "fitV") viewer.viewport.fitVertically();
      if (type === "fitH") viewer.viewport.fitHorizontally();
    };

    const changePage = (target) => {
      context.emit("changePage", target);
    };

    const changeSplitView = () => {
      context.emit("toggleSplitter");
    };

    const changeDrawerMini = () => {
      context.emit("toggleDrawer");
    };

    const loadPage = () => {
      if (!isEmpty(currentPageData.value)) {
        viewer.open(currentPageData.value.manifestUrl);
        viewer.viewport.zoomTo(defaultZoomLevel.value);
      }
    };

    onMounted(async () => {
      await nextTick();
      viewer = markRaw(
        OpenSeadragon({
          id: "viewer-container",
          animationTime: 0.4,
          immediateRender: true,
          preserveImageSizeOnResize: true,
          showNavigationControl: false,
          showZoomControl: false,
          preserveViewport: true,
          visibilityRatio: 1,
          minZoomLevel: minZoomLevel.value,
          maxZoomLevel: maxZoomLevel.value,
          defaultZoomLevel: defaultZoomLevel.value,
          sequenceMode: false,
          crossOriginPolicy: "Anonymous",
          prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
          tileSources: [currentPageData.value.manifestUrl],
        }),
      );
      if (currentPageData.value.viewerZoom) {
        viewer.viewport.zoomTo(currentPageData.value.viewerZoom);
      } else {
        currentPageData.value.viewerZoom = viewer.viewport.getZoom(true);
      }
      viewer.addHandler("zoom", (evt) => {
        currentPageData.value.viewerZoom = evt.zoom;
      });
    });

    watch(
      () => view.value.currentPageRef,
      () => loadPage(),
    );

    onBeforeUnmount(() => {
      viewer.destroy();
      viewer = null; // https://openseadragon.github.io/docs/OpenSeadragon.Viewer.html#destroy
    });

    return {
      changePage,
      changeSplitView,
      changeDrawerMini,
      currentPageData,
      pageCount,
      minZoomLevel,
      maxZoomLevel,
      navPosition,
      toolPosition,
      zoomPosition,
      tbHorAlt,
      tbVertAlt,
      viewerHeight,
      viewerWidth,
      view,
      zoom,
    };
  },
});
</script>

<style lang="scss" scoped>
/* container */
#viewer-container {
  display: inline-flex;
  background-color: #474747;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  transition: height 0.2s ease-in-out;
}
.q-splitter--vertical #viewer-container {
  border-right: none;
  border-top-right-radius: 0;
  border-bottom-left-radius: 3px;
}
/* toolbar */
.viewer-toolbar {
  display: flex;
  position: absolute;
  z-index: 2;
  background-color: rgba(0, 0, 0, 0.75);
  align-items: center;
  border-radius: 4px;
}
.viewer-toolbar.toolbar-h {
  flex-direction: row;
  height: 32px;
  padding: 0 1px;
}
.viewer-toolbar.toolbar-v {
  flex-direction: column;
  width: 32px;
  padding: 1px 0;
}
.viewer-toolbar button {
  color: #d4d4d4;
  font-size: 11px;
  padding: 4px;
  height: 30px;
  width: 30px;
  border-radius: 0;
  border-right: 1px solid #717171;
}
.viewer-toolbar button::before {
  box-shadow: none;
}
.viewer-toolbar.toolbar-v button {
  border-right: none;
  border-bottom: 1px solid #717171;
}
.viewer-toolbar.toolbar-v button:last-of-type {
  border-bottom: none;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
}
.viewer-toolbar.toolbar-v button:first-of-type {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}
.viewer-toolbar.tb-zoom button.zoom-btn i {
  font-size: 1.9em !important;
  padding-top: 1px;
}
.viewer-toolbar.toolbar-h button:last-of-type {
  border-right: none;
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}
.viewer-toolbar.toolbar-h button:first-of-type {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}
.viewer-current-page {
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1.1rem;
  letter-spacing: 0.0125em;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.viewer-toolbar.toolbar-h .viewer-current-page {
  border-right: 1px solid #717171;
  height: 30px;
  padding: 0 12px;
}
.viewer-toolbar.toolbar-v .viewer-current-page {
  border-top: 1px solid #717171;
  width: 30px;
  padding: 12px 0;
  transform: rotate(180deg);
  writing-mode: tb;
}
/* crossed-out icon */
.crossed-out .q-btn__content::after {
  content: "";
  width: 2px;
  height: 75%;
  background: #c3c3c3;
  transform: rotate(35deg);
  position: absolute;
}
</style>
