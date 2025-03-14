import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { EventBus, debounce } from "quasar";

export const useUiStore = defineStore(
  "ui",
  () => {
    // event bus
    const eventBus = new EventBus();

    // state
    const previousPath = ref("");
    const currentPath = ref("");
    const currentSection = ref("");
    const currentSubsection = ref("");
    const breadcrumbTail = ref([]);
    const currentPageIcon = ref("");
    const globalLoading = ref(false);
    const isFullscreen = ref(false);
    const userDrawerOpen = ref(false);
    const appDrawerOpen = ref(false);
    const windowHeight = ref(window.innerHeight);
    const windowWidth = ref(window.innerWidth);
    const drawerExpanded = ref(false);
    const pageIndexShow = ref(false);
    const inlineIndexShow = ref(false);
    const windowIndexShow = ref(false);
    const currentPageEdit = ref(false);

    // getters
    const breadcrumb = computed(() => {
      const bc = [currentSection.value];
      if (currentSubsection.value) bc.push(currentSubsection.value);
      return bc.concat(breadcrumbTail.value);
    });

    const isSameRoute = computed(() => previousPath.value === currentPath.value);

    const contentHeight = computed(() => {
      const headerHeight = 117;
      const footerSpace = 40;
      return windowHeight.value - headerHeight - footerSpace;
    });

    const contentWidth = computed(() => {
      const padding = 68;
      return windowWidth.value - padding;
    });

    // actions
    const $reset = () => {
      // eventBus.value = new EventBus();
      previousPath.value = "";
      currentPath.value = "";
      currentSection.value = "";
      currentSubsection.value = "";
      breadcrumbTail.value = [];
      currentPageIcon.value = "";
      globalLoading.value = false;
      isFullscreen.value = false;
      userDrawerOpen.value = false;
      appDrawerOpen.value = false;
      windowHeight.value = window.innerHeight;
      windowWidth.value = window.innerWidth;
      drawerExpanded.value = false;
      pageIndexShow.value = false;
      inlineIndexShow.value = false;
      windowIndexShow.value = false;
      currentPageEdit.value = false;
    };

    const onWindowResize = () => {
      windowHeight.value = window.innerHeight;
      windowWidth.value = window.innerWidth;
    };

    const resizeListener = () => {
      window.addEventListener("resize", debounce(onWindowResize, 30));
    };

    const setUiState = () => {
      drawerExpanded.value = isSameRoute.value ? drawerExpanded.value : false;
      currentPageEdit.value = isSameRoute.value ? currentPageEdit.value : false;
    };

    const resetBreadcrumbTail = () => {
      breadcrumbTail.value = [];
    };

    const setPageState = async (target) => {
      previousPath.value = currentPath.value;
      currentPath.value = target.fullPath;
      currentSection.value = target.meta.navPath ? target.meta.navPath[0] : undefined;
      currentSubsection.value = target.meta.navPath ? target.meta.navPath[1] : undefined;
      currentPageIcon.value = target.meta.pageIcon
        ? target.meta.pageIcon
        : target.meta.icon || "mdi-layers";
      resetBreadcrumbTail();
    };

    return {
      eventBus,
      previousPath,
      currentPath,
      currentSection,
      currentSubsection,
      breadcrumbTail,
      currentPageIcon,
      globalLoading,
      isFullscreen,
      userDrawerOpen,
      appDrawerOpen,
      windowHeight,
      windowWidth,
      drawerExpanded,
      pageIndexShow,
      inlineIndexShow,
      windowIndexShow,
      currentPageEdit,
      breadcrumb,
      isSameRoute,
      contentHeight,
      contentWidth,
      onWindowResize,
      resizeListener,
      setUiState,
      resetBreadcrumbTail,
      setPageState,
      $reset,
    };
  },
  {
    persist: {
      afterRestore: (ctx) => {
        ctx.store.resetBreadcrumbTail();
      },
    },
  },
);
