<template>
  <div id="viewer-container" :style="`height: ${viewerHeight}px; width: ${viewerWidth}px`">
    <div
      v-if="Records.pageCount > 1"
      @mouseleave="expandNav = false"
      @mouseover="expandNav = true"
      :class="`hot-zone nav ${tbVertAlt ? 'toolbar-v' : 'toolbar-h'}`"
      :style="navPosition"
    >
      <div :class="`viewer-toolbar ${tbVertAlt ? 'toolbar-v' : 'toolbar-h'}`">
        <div class="nav-arrows">
          <transition
            :enter-active-class="`animated ${tbVertAlt ? 'fadeInUp' : 'fadeInRight'} delay-1s`"
            :leave-active-class="`animated ${tbVertAlt ? 'fadeOutDown' : 'fadeOutRight'}`"
            appear
          >
            <div v-show="expandNav">
              <q-btn
                @click="changePage('first')"
                :disabled="Records.currentPageIndex === 0"
                class="start"
                icon="first_page"
              />
              <q-btn
                @click="changePage('prev')"
                :disabled="Records.currentPageIndex === 0"
                icon="navigate_before"
              />
            </div>
          </transition>
        </div>
        <div class="viewer-current-page">{{ Records.currentPage.name }}</div>
        <div class="nav-arrows">
          <transition
            :enter-active-class="`animated ${tbVertAlt ? 'fadeInDown' : 'fadeInLeft'}  delay-1s`"
            :leave-active-class="`animated ${tbVertAlt ? 'fadeOutUp' : 'fadeOutLeft'}`"
            appear
          >
            <div v-show="expandNav">
              <q-btn
                @click="changePage('next')"
                :disabled="Records.currentPageIndex === Records.pageCount - 1"
                icon="navigate_next"
              />
              <q-btn
                @click="changePage('last')"
                :disabled="Records.currentPageIndex === Records.pageCount - 1"
                class="end"
                icon="last_page"
              />
            </div>
          </transition>
        </div>
      </div>
    </div>
    <div
      @mouseleave="expandTools = false"
      @mouseover="expandTools = true"
      :class="`hot-zone tools ${tbHorAlt ? 'zoombar-h' : 'zoombar-v'}`"
    >
      <q-btn
        @click="changeSplitView"
        :icon="Records.splitterHorizontal ? 'o_border_vertical' : 'o_border_horizontal'"
        class="pivot"
      />
      <transition
        :enter-active-class="`animated ${tbHorAlt ? 'fadeInLeft' : 'fadeInDown'} delay-1s`"
        :leave-active-class="`animated ${tbHorAlt ? 'fadeOutLeft' : 'fadeOutUp'}`"
        appear
      >
        <div
          v-show="expandTools"
          :class="`viewer-toolbar tb-zoom ${tbHorAlt ? 'toolbar-h' : 'toolbar-v'}`"
          :style="zoomPosition"
        >
          <q-btn
            @click="zoom('in')"
            :class="`${tbHorAlt ? 'zoom-btn' : 'zoom-btn start'}`"
            :disabled="Records.viewerZoom >= maxZoomLevel"
            icon="zoom_in"
          />
          <q-btn
            @click="zoom('out')"
            :disabled="Records.viewerZoom <= minZoomLevel"
            class="zoom-btn"
            icon="zoom_out"
          />
          <q-btn @click="zoom('full')" icon="aspect_ratio" />
          <q-btn @click="zoom('fitV')" icon="expand" />
          <q-btn @click="zoom('fitH')" class="end">
            <q-icon class="rotate-90" name="expand" />
          </q-btn>
        </div>
      </transition>
      <transition
        enter-active-class="animated fadeInLeft delay-1s"
        leave-active-class="animated fadeOutLeft"
        appear
      >
        <div v-show="expandTools" :style="toolPosition" class="viewer-toolbar toolbar-h">
          <q-btn
            v-if="Records.pageCount > 1"
            @click="changeDrawerMini"
            :class="drawerButtonClasses"
            icon="o_auto_stories"
          />
        </div>
      </transition>
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

import { Records } from "@/models";

export default defineComponent({
  name: "IiifViewer",
  emits: ["changePage", "toggleSplitter", "toggleDrawer"],
  setup(_, context) {
    var viewer = null;
    const { viewerHeight, viewerWidth } = inject("viewerDimensions");
    const expandNav = ref(false);
    const expandTools = ref(false);

    const tbHorAlt = computed(() => Records.splitterHorizontal && viewerHeight.value < 198);
    const tbVertAlt = computed(() => !Records.splitterHorizontal && viewerWidth.value < 240);
    const navPosition = computed(() => {
      let top = tbVertAlt.value ? 199 : 5;
      let posHor = tbVertAlt.value ? "left" : "right";
      return `top: ${top}px; ${posHor}: 5px`;
    });
    const toolPosition = computed(() => `top: -1px; left: ${tbHorAlt.value ? -153 : -33}px`);
    const zoomPosition = computed(() => {
      let top = tbHorAlt.value ? -1 : 29;
      let left = tbHorAlt.value ? (Records.pageCount > 1 ? 29 : 0) : -31;
      return `top: ${top}px; left: ${left}px`;
    });
    const drawerButtonClasses = computed(() => {
      const cls = ["border-left"];
      tbHorAlt.value ? cls.push("border-right") : cls.push("end");
      if (Records.pageDrawerMini) cls.push("crossed-out");
      return cls.join(" ");
    });

    const minZoomLevel = ref(0.5);
    const maxZoomLevel = ref(8);
    const defaultZoomLevel = computed(() => (Records.viewerZoom ? Records.viewerZoom : 1));

    const zoom = (type) => {
      if (type === "full") console.log("FULL ZOOM");
      if (type === "out") {
        let level = Records.viewerZoom - 0.25;
        if (level <= minZoomLevel.value) level = minZoomLevel.value;
        viewer.viewport.zoomTo(level);
      }
      if (type === "in") {
        let level = Records.viewerZoom + 0.25;
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
      if (!isEmpty(Records.currentPage)) {
        viewer.open(Records.currentPage.manifestUrl);
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
          tileSources: [Records.currentPage.manifestUrl],
        }),
      );
      if (Records.viewerZoom) {
        viewer.viewport.zoomTo(Records.viewerZoom);
      } else {
        Records.viewerZoom = viewer.viewport.getZoom(true);
      }
      viewer.addHandler("zoom", (evt) => {
        console.log("storing zoom", evt.zoom);
        Records.viewerZoom = evt.zoom;
      });
    });

    watch(
      () => Records.currentState.currentPageId,
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
      minZoomLevel,
      maxZoomLevel,
      navPosition,
      toolPosition,
      zoomPosition,
      tbHorAlt,
      tbVertAlt,
      viewerHeight,
      viewerWidth,
      zoom,
      expandNav,
      expandTools,
      drawerButtonClasses,
      Records,
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
  cursor: grab;
}
.q-splitter--vertical #viewer-container {
  border-right: none;
  border-top-right-radius: 0;
  border-bottom-left-radius: 3px;
}
/* toolbars general */
.viewer-toolbar {
  display: flex;
  position: relative;
  z-index: 2;
  align-items: center;
  border-radius: 4px;
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
  cursor: default;
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.25);
  transition:
    transform 0.3s ease-in-out,
    border-radius 0.1s ease-in-out;
}
.viewer-toolbar button,
.pivot {
  color: #d4d4d4;
  font-size: 11px;
  padding: 4px;
  height: 30px;
  width: 30px;
  min-height: 30px;
  min-width: 30px;
}
.border-left {
  border-left: 1px solid #717171;
}
.border-right {
  border-right: 1px solid #717171 !important;
}
.viewer-toolbar button:not(.pivot) {
  border-right: 1px solid #717171;
  border-radius: 0;
}
.viewer-toolbar button::before {
  box-shadow: none;
}
.viewer-toolbar .q-btn {
  background-color: rgba(0, 0, 0, 0.75);
}
.viewer-toolbar.tb-zoom button.zoom-btn i {
  font-size: 1.9em !important;
  padding-top: 1px;
}
.crossed-out .q-btn__content::after {
  content: "";
  width: 2px;
  height: 75%;
  background: #c3c3c3;
  transform: rotate(35deg);
  position: absolute;
}
.hot-zone {
  position: absolute;
  display: flex;
  z-index: 99;
}
.pivot {
  border-radius: 3px;
  background-color: rgba(0, 0, 0, 0.25) !important;
  transition: all 0.3s ease-in-out;
}
.hot-zone:hover .pivot {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  background-color: rgba(0, 0, 0, 0.75) !important;
}
/* toolbars horizontal */
.viewer-toolbar.toolbar-h {
  flex-direction: row;
  height: 32px;
  padding: 0 1px;
}
.viewer-toolbar.toolbar-h .viewer-current-page {
  transform: translateX(60px);
}
.viewer-toolbar.toolbar-h .nav-arrows {
  width: 60px;
}
.viewer-toolbar.toolbar-h .start {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}
.viewer-toolbar.toolbar-h .end {
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}
.viewer-toolbar.toolbar-h button:last-of-type {
  border-right: none;
}
.viewer-toolbar.toolbar-h .viewer-current-page {
  height: 30px;
  padding: 0 12px;
}
.hot-zone.nav.toolbar-h {
  height: 100px;
  width: 200px;
  justify-content: end;
}
.hot-zone.tools {
  height: 200px;
  width: 100px;
  justify-content: start;
  top: 5px;
  left: 5px;
}
.hot-zone.tools.zoombar-h {
  height: 80px;
  width: 250px;
}
.hot-zone.nav.toolbar-h:hover .viewer-current-page {
  border-radius: 0;
  background-color: rgba(0, 0, 0, 0.75);
  border-right: 1px solid #717171;
  border-left: 1px solid #717171;
  transform: translateX(0);
}

/* vertical toolbars */
.viewer-toolbar.toolbar-v {
  flex-direction: column;
  width: 32px;
  padding: 1px 0;
}
.viewer-toolbar.toolbar-v button {
  border-right: none;
  border-bottom: 1px solid #717171;
}
.viewer-toolbar.toolbar-v .start {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
}
.viewer-toolbar.toolbar-v .end {
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
}
.viewer-toolbar.toolbar-v .zoom-btn.start {
  border-radius: 0;
  border-top: 1px solid #717171;
}
.viewer-toolbar.toolbar-v button:last-of-type {
  border-bottom: none;
}
.viewer-toolbar.toolbar-v .viewer-current-page {
  width: 30px;
  padding: 12px 0;
  transform: rotate(180deg);
  writing-mode: tb;
}
.viewer-toolbar.toolbar-v .nav-arrows {
  height: 60px;
  width: 30px;
}
.hot-zone.nav.toolbar-v {
  height: 200px;
  width: 100px;
  justify-content: start;
}
.hot-zone.nav.toolbar-v:hover .viewer-current-page {
  border-radius: 0;
  background-color: rgba(0, 0, 0, 0.75);
  border-top: 1px solid #717171;
  border-bottom: 1px solid #717171;
}
</style>
