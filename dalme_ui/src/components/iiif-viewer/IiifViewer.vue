<template>
  <div
    id="viewer-container"
    :style="`height: ${viewerHeight}px; width: ${viewerWidth}px`"
  >
    <div
      v-if="view.folioCount > 1"
      :class="`viewer-toolbar ${tbVertAlt ? 'toolbar-v' : 'toolbar-h'}`"
      :style="navPosition"
    >
      <q-btn
        :disabled="view.currentFolio === 0"
        icon="first_page"
        @click="changeFolio('first')"
      />
      <q-btn
        :disabled="view.currentFolio === 0"
        icon="navigate_before"
        @click="changeFolio('prev')"
      />
      <div class="viewer-current-folio">{{ cFolio.name }}</div>
      <q-btn
        :disabled="view.currentFolio === view.folioCount - 1"
        icon="navigate_next"
        @click="changeFolio('next')"
      />
      <q-btn
        :disabled="view.currentFolio === view.folioCount - 1"
        icon="last_page"
        @click="changeFolio('last')"
      />
    </div>
    <div
      :class="`viewer-toolbar tb-zoom ${tbHorAlt ? 'toolbar-h' : 'toolbar-v'}`"
      :style="zoomPosition"
    >
      <q-btn
        icon="zoom_in"
        @click="zoom('in')"
        class="zoom-btn"
        :disabled="cFolio.viewerZoom >= maxZoomLevel"
      />
      <q-btn
        icon="zoom_out"
        @click="zoom('out')"
        class="zoom-btn"
        :disabled="cFolio.viewerZoom <= minZoomLevel"
      />
      <q-btn icon="aspect_ratio" @click="zoom('full')" />
      <q-btn icon="expand" @click="zoom('fitV')" />
      <q-btn @click="zoom('fitH')">
        <q-icon name="expand" class="rotate-90" />
      </q-btn>
    </div>
    <div class="viewer-toolbar toolbar-h" :style="toolPosition">
      <q-btn
        :icon="
          view.splitterHorizontal ? 'o_border_vertical' : 'o_border_horizontal'
        "
        @click="changeSplitView"
      />
      <q-btn
        v-if="view.folioCount > 1"
        icon="o_auto_stories"
        :class="view.folioDrawerMini ? '' : 'crossed-out'"
        @click="changeDrawerMini"
      />
    </div>
  </div>
</template>

<script>
import { isEmpty } from "ramda";
import {
  computed,
  defineComponent,
  inject,
  markRaw,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from "vue";
import { useStores } from "@/use";
import OpenSeadragon from "openseadragon";

export default defineComponent({
  name: "IiifViewer",
  emits: ["changeFolio", "toggleSplitter", "toggleDrawer"],
  setup(_, context) {
    var viewer = null;
    const { viewerHeight, viewerWidth } = inject("viewerDimensions");
    const { view } = useStores();
    const cFolio = computed(() => view.value.folios[view.value.currentFolio]);

    const tbHorAlt = computed(
      () => view.value.splitterHorizontal && viewerHeight.value < 198,
    );
    const tbVertAlt = computed(
      () => !view.value.splitterHorizontal && viewerWidth.value < 240,
    );
    const navPosition = computed(() => {
      let top = tbVertAlt.value ? 199 : 5;
      let posHor = tbVertAlt.value ? "left" : "right";
      return `top: ${top}px; ${posHor}: 5px`;
    });
    const toolPosition = computed(() => "top: 5px; left: 5px");
    const zoomPosition = computed(() => {
      let top = tbHorAlt.value ? 5 : 42;
      let left = tbHorAlt.value ? (view.value.folioCount > 1 ? 71 : 41) : 5;
      return `top: ${top}px; left: ${left}px`;
    });

    const minZoomLevel = ref(0.5);
    const maxZoomLevel = ref(8);
    const defaultZoomLevel = computed(() =>
      cFolio.value.viewerZoom ? cFolio.value.viewerZoom : 0,
    );

    const zoom = (type) => {
      if (type === "full") console.log(cFolio.value.ref - 1);
      if (type === "out") {
        let level = cFolio.value.viewerZoom - 0.25;
        if (level <= minZoomLevel.value) level = minZoomLevel.value;
        viewer.viewport.zoomTo(level);
      }
      if (type === "in") {
        let level = cFolio.value.viewerZoom + 0.25;
        if (level >= maxZoomLevel.value) level = maxZoomLevel.value;
        viewer.viewport.zoomTo(level);
      }
      if (type === "fitV") viewer.viewport.fitVertically();
      if (type === "fitH") viewer.viewport.fitHorizontally();
    };

    const changeFolio = (target) => {
      context.emit("changeFolio", target);
    };

    const changeSplitView = () => {
      context.emit("toggleSplitter");
    };

    const changeDrawerMini = () => {
      context.emit("toggleDrawer");
    };

    const loadFolio = () => {
      if (!isEmpty(view.value)) {
        viewer.open(cFolio.value.manifestUrl);
        viewer.viewport.zoomTo(defaultZoomLevel.value);
      }
    };

    onMounted(() => {
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
          prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
          tileSources: [cFolio.value.manifestUrl],
        }),
      );
      if (cFolio.value.viewerZoom) {
        viewer.viewport.zoomTo(cFolio.value.viewerZoom);
      } else {
        cFolio.value.viewerZoom = viewer.viewport.getZoom(true);
      }
      viewer.addHandler("zoom", (evt) => {
        cFolio.value.viewerZoom = evt.zoom;
      });
    });

    watch(
      () => view.value.currentFolio,
      () => loadFolio(),
    );

    onBeforeUnmount(() => {
      viewer.destroy();
      viewer = null; // https://openseadragon.github.io/docs/OpenSeadragon.Viewer.html#destroy
    });

    return {
      changeFolio,
      changeSplitView,
      changeDrawerMini,
      cFolio,
      minZoomLevel,
      maxZoomLevel,
      navPosition,
      toolPosition,
      zoomPosition,
      tbHorAlt,
      tbVertAlt,
      view,
      viewerHeight,
      viewerWidth,
      zoom,
    };
  },
});
</script>

<style lang="scss">
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
.viewer-current-folio {
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1.1rem;
  letter-spacing: 0.0125em;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}
.viewer-toolbar.toolbar-h .viewer-current-folio {
  border-right: 1px solid #717171;
  height: 30px;
  padding: 0 12px;
}
.viewer-toolbar.toolbar-v .viewer-current-folio {
  border-top: 1px solid #717171;
  width: 30px;
  padding: 12px 0;
  transform: rotate(180deg);
  writing-mode: tb;
}
#viewer-container {
  display: inline-flex;
  background-color: #474747;
  border-top: 1px solid #919191;
  border-left: 1px solid #919191;
  border-right: 1px solid #919191;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
.q-splitter--vertical #viewer-container {
  border-right: none;
  border-top-right-radius: 0;
  border-bottom-left-radius: 4px;
  border-bottom: 1px solid #919191;
}
.openseadragon-canvas {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}
.q-splitter--vertical .openseadragon-canvas {
  border-top-right-radius: 0;
  border-bottom-left-radius: 3px;
}
.crossed-out .q-btn__content::after {
  content: "";
  width: 2px;
  height: 75%;
  background: #c3c3c3;
  transform: rotate(35deg);
  position: absolute;
}
</style>
