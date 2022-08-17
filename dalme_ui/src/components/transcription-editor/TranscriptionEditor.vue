<template>
  <div v-if="!localLoading">
    <q-card>
      <q-splitter v-model="editorSplitter" horizontal style="height: 800px">
        <template v-slot:before>
          <IIIFViewer />
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
    <OpaqueSpinner :showing="localLoading" />
  </div>
</template>

<script>
import { defineComponent, inject, provide, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { sourceDetailSchema, transcriptionsFieldSchema } from "@/schemas";
import { useAPI } from "@/use";
import { VAceEditor } from "vue3-ace-editor";
import "ace-builds/src-noconflict/mode-xml";
import "ace-builds/src-noconflict/theme-chrome";
import { IIIFViewer } from "@/components";

export default defineComponent({
  name: "TranscriptionEditor",
  components: {
    OpaqueSpinner,
    VAceEditor,
    IIIFViewer,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const id = inject("id");
    const localLoading = ref(true);

    const folios = ref([]);
    const currentFolio = ref(0);
    const updateCurrentFolio = (value) => {
      currentFolio.value = value;
    };

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

    const fetchData = async () => {
      await fetchAPI(requests.sources.getSource(id.value));
      if (success.value)
        await sourceDetailSchema
          .validate(data.value, { stripUnknown: false })
          .then((value) => {
            folios.value = value.pages;
            fetchTranscription(folios.value[0].transcriptionId);
            localLoading.value = false;
          });
    };

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
    provide("id", id);
    provide("fetchTranscription", fetchTranscription);
    provide("folios", folios);
    provide("currentFolio", {
      currentFolio,
      updateCurrentFolio,
    });

    watch(
      () => $route.params.id,
      async (to) => {
        if (to) {
          id.value = to;
          await fetchData();
        }
      },
      { immediate: true },
    );

    return {
      editorSplitter,
      localLoading,
      editorContent,
      IIIFViewer,
    };
  },
});
</script>
