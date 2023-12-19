import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useViewStore } from "@/stores/views";
import { useAuthStore } from "@/stores/auth";
import { EventBus } from "quasar";

export const useUiStore = defineStore(
  "ui",
  () => {
    // stores
    const auth = useAuthStore();

    // event bus
    const eventBus = new EventBus();

    // state
    // const eventBus = ref(new EventBus());
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
    const stripExpanded = ref(false);
    const stripKeepOpen = ref(false);
    const drawerExpanded = ref(false);
    const folioIndexShow = ref(false);
    const inlineIndexShow = ref(false);
    const windowIndexShow = ref(false);
    const currentFolioEdit = ref(false);
    const stripApproachHover = ref(false);

    // getters
    const breadcrumb = computed(() => {
      const bc = [currentSection.value];
      if (currentSubsection.value) bc.push(currentSubsection.value);
      return bc.concat(breadcrumbTail.value);
    });

    const isSameRoute = computed(() => previousPath.value === currentPath.value);

    const containerHeight = computed(() => {
      const headerHeight = 279;
      const chrome = headerHeight + 32;
      return windowHeight.value - chrome;
    });

    const containerWidth = computed(() => {
      const views = useViewStore();
      let chrome = 84;
      if ("folioDrawerMini" in views.view && views.view.folioDrawerMini.value)
        chrome = chrome + 149;
      return windowWidth.value - chrome;
    });

    const showTips = computed({
      get() {
        return auth.preferences.general.tooltipsOn;
      },
      set(newValue) {
        auth.preferences.general.tooltipsOn = newValue;
      },
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
      stripExpanded.value = false;
      stripKeepOpen.value = false;
      drawerExpanded.value = false;
      folioIndexShow.value = false;
      inlineIndexShow.value = false;
      windowIndexShow.value = false;
      currentFolioEdit.value = false;
      stripApproachHover.value = false;
    };

    const onWindowResize = () => {
      windowHeight.value = window.innerHeight;
      windowWidth.value = window.innerWidth;
    };

    const resizeListener = () => {
      window.addEventListener("resize", onWindowResize);
    };

    const setUiState = () => {
      stripExpanded.value = stripKeepOpen.value ? true : false;
      drawerExpanded.value = isSameRoute.value ? drawerExpanded.value : false;
      currentFolioEdit.value = isSameRoute.value ? currentFolioEdit.value : false;
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
      stripExpanded,
      stripKeepOpen,
      drawerExpanded,
      folioIndexShow,
      inlineIndexShow,
      windowIndexShow,
      currentFolioEdit,
      stripApproachHover,
      breadcrumb,
      isSameRoute,
      containerHeight,
      containerWidth,
      onWindowResize,
      resizeListener,
      setUiState,
      resetBreadcrumbTail,
      setPageState,
      $reset,
      showTips,
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
