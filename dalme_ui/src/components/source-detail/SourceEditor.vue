<template>
  <q-card>
    <SourceEditorToolbar />
    <q-splitter v-model="editorSplitter" horizontal style="height: 800px">
      <template v-slot:before>
        <SourceImageViewer />
      </template>

      <template v-slot:separator>
        <q-btn
          square
          color="primary"
          text-color="white"
          size="xs"
          padding="xs md"
          icon="drag_handle"
        />
      </template>

      <template v-slot:after>
        <v-ace-editor
          v-model:value="editorContent"
          lang="xml"
          theme="chrome"
          style="height: 300px"
        />
      </template>
    </q-splitter>
  </q-card>
</template>

<script>
import { defineComponent, inject, onMounted, provide, ref } from "vue";
import { requests } from "@/api";
import { transcriptionsFieldSchema } from "@/schemas";
import { useAPI } from "@/use";
import { VAceEditor } from "vue3-ace-editor";
import "ace-builds/src-noconflict/mode-xml";
import "ace-builds/src-noconflict/theme-chrome";
import SourceEditorToolbar from "./SourceEditorToolbar.vue";
import SourceImageViewer from "./SourceImageViewer.vue";

export default defineComponent({
  name: "SourceEditor",
  components: {
    VAceEditor,
    SourceImageViewer,
    SourceEditorToolbar,
  },
  setup() {
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const pages = inject("pages");
    const localLoading = ref(true);
    // const { currentFolio, updateCurrentFolio } = inject("currentFolio");

    const editorSplitter = ref(50);
    const editorContent = ref("");

    const viewerOptions = ref({
      id: "viewer-container",
      animationTime: 0.4,
      immediateRender: true,
      preserveImageSizeOnResize: true,
      showNavigationControl: false,
      showZoomControl: false,
      preserveViewport: true,
      visibilityRatio: 1,
      minZoomLevel: 1,
      defaultZoomLevel: 1,
      sequenceMode: true,
      prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
      tileSources: [],
    });

    const fetchTranscription = async (tr_id) => {
      await fetchAPI(requests.transcriptions.getTranscription(tr_id));
      if (success.value)
        await transcriptionsFieldSchema
          .validate(data.value, { stripUnknown: true })
          .then((tr_value) => {
            editorContent.value = tr_value.transcription;
          });
    };

    provide("viewerOptions", viewerOptions);
    provide("fetchTranscription", fetchTranscription);

    onMounted(async () => {
      localLoading.value = true;
      await fetchTranscription(pages[0].transcriptionId).then(() => {
        localLoading.value = false;
      });
    });

    return {
      editorSplitter,
      localLoading,
      editorContent,
    };
  },
});
</script>
