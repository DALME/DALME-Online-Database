// Define the records store
import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { Records } from "@/models";

const defaultRecordState = {
  currentPageId: null,
  editOn: false,
  editorSplitter: null,
  lastSplitter: null,
  pageDrawerMini: false,
  showTagMenu: false,
  splitterHorizontal: false,
  tab: "info",
  pageStates: {},
};

const defaultPageState = {
  editorTab: "preview",
  viewerZoom: 0,
  editorContent: null,
};

export const useRecordStore = defineStore(
  "records",
  () => {
    // stores and repositories
    window.testRecordRepo = Records;

    // state
    const currentRecordId = ref(null);
    const recordStates = ref({});

    // getters
    const current = computed(() =>
      currentRecordId.value ? Records.withAllRecursive().find(currentRecordId.value) : null,
    );

    const currentRecordState = computed(() => {
      if (!currentRecordId.value) return defaultRecordState;
      if (currentRecordId.value && !recordStates.value[currentRecordId.value])
        recordStates.value[currentRecordId.value] = defaultRecordState;
      return recordStates.value[currentRecordId.value];
    });

    const currentPage = computed(() =>
      currentRecordId.value
        ? current.value.pages.find((p) => p.id === currentRecordState.value.currentPageId)
        : null,
    );

    const currentPageIndex = computed(() =>
      currentRecordId.value ? current.value.pages.indexOf(currentPage.value) : null,
    );

    const currentPageState = computed(() => {
      if (!currentRecordId.value) return defaultPageState;
      if (!currentRecordState.value.pageStates[currentRecordState.value.currentPageId])
        currentRecordState.value.pageStates[currentRecordState.value.currentPageId] =
          defaultPageState;
      return currentRecordState.value.pageStates[currentRecordState.value.currentPageId];
    });

    const pageCount = computed(() => (currentRecordId.value ? current.value.pages.length : 0));

    // getters/setters for current record state props
    const currentPageId = computed({
      get: () => {
        if (!currentRecordId.value) return null;
        if (!currentRecordState.value.currentPageId)
          currentRecordState.value.currentPageId = current.value.pages[0].id;
        return currentRecordState.value.currentPageId;
      },
      set: (value) => (currentRecordState.value.currentPageId = value),
    });
    const editOn = computed({
      get: () => currentRecordState.value.editOn,
      set: (value) => (currentRecordState.value.editOn = value),
    });
    const editorSplitter = computed({
      get: () => currentRecordState.value.editorSplitter,
      set: (value) => (currentRecordState.value.editorSplitter = value),
    });
    const lastSplitter = computed({
      get: () => currentRecordState.value.lastSplitter,
      set: (value) => (currentRecordState.value.lastSplitter = value),
    });
    const pageDrawerMini = computed({
      get: () => currentRecordState.value.pageDrawerMini,
      set: (value) => (currentRecordState.value.pageDrawerMini = value),
    });
    const showTagMenu = computed({
      get: () => currentRecordState.value.showTagMenu,
      set: (value) => (currentRecordState.value.showTagMenu = value),
    });
    const splitterHorizontal = computed({
      get: () => currentRecordState.value.splitterHorizontal,
      set: (value) => (currentRecordState.value.splitterHorizontal = value),
    });
    const tab = computed({
      get: () => currentRecordState.value.tab,
      set: (value) => (currentRecordState.value.tab = value),
    });

    // getters/setters for current page state props
    const editorTab = computed({
      get: () => currentPageState.value.editorTab,
      set: (value) => (currentPageState.value.editorTab = value),
    });
    const viewerZoom = computed({
      get: () => currentPageState.value.viewerZoom,
      set: (value) => (currentPageState.value.viewerZoom = value),
    });
    const editorContent = computed({
      get: () => {
        console.log(
          "CURRENT PAGE",
          currentRecordId.value,
          current.value,
          currentPageId.value,
          currentPage.value,
        );
        if (!currentPageState.value.editorContent)
          currentPageState.value.editorContent = currentPage.value.transcription.transcription;
        return currentPageState.value.editorContent;
      },
      set: (value) => (currentPageState.value.editorContent = value),
    });

    // actions
    const setCurrent = (id) =>
      new Promise((resolve) => {
        Records.ensure(id).then(() => {
          currentRecordId.value = id;
          resolve();
        });
      });

    return {
      currentRecordId,
      current,
      setCurrent,
      currentPage,
      currentPageId,
      editOn,
      editorSplitter,
      lastSplitter,
      pageDrawerMini,
      showTagMenu,
      splitterHorizontal,
      tab,
      editorTab,
      viewerZoom,
      editorContent,
      pageCount,
      currentPageIndex,
      Records,
    };
  },
  {
    persist: true,
  },
);
