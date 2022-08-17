<template>
  <div class="iiif-viewer" tabindex="-1">
    <ViewerToolbar />
    <div id="viewer-container" style="height: 400px"></div>
  </div>
</template>

<script>
import { computed, inject, defineComponent, onMounted, ref } from "vue";
import { useAPI } from "@/use";
import { requests } from "@/api";
import OpenSeadragon from "openseadragon";
import ViewerToolbar from "./ViewerToolbar";

export default defineComponent({
  name: "iiif-viewer",
  components: { ViewerToolbar },

  setup() {
    const { apiInterface } = useAPI();
    const { success, data, fetchAPI } = apiInterface();
    const viewer = ref(null);
    const manifest = ref({});
    const options = inject("viewerOptions");
    const sourceId = inject("id");
    const folios = inject("folios");
    const { currentFolio, updateCurrentFolio } = inject("currentFolio");
    const fetchTranscription = inject("fetchTranscription");

    const canvases = computed(() => {
      return manifest.value.sequences[0].canvases;
    });

    const folioCount = computed(() => {
      return manifest.value.sequences[0].canvases.length;
    });

    const fetchManifest = async () => {
      await fetchAPI(requests.sources.getSourceManifest(sourceId.value));
      if (success.value) {
        if (isManifest(data.value)) {
          manifest.value = data.value;
          loadImageInfo().then(() => {
            viewer.value = OpenSeadragon(options.value);
            viewer.value.addHandler("page", (event) => {
              updateCurrentFolio(event.page);
              fetchTranscription(
                folios.value[currentFolio.value].transcriptionId,
              );
            });

            // new OpenSeadragon.MouseTracker({
            //     element: this.viewer.canvas,
            //     pressHandler: this.pressHandler,
            //     dragHandler: this.dragHandler,
            //     dragEndHandler: this.dragEndHandler
            // }).setTracking(true);
            //
            // window.onresize = () => {
            //     overlay.resize();
            //     overlay.resizecanvas();
            // };
          });
        }
      }
    };

    const loadImageInfo = async () => {
      for (let i = 0; i < folioCount.value; i++) {
        const { resource } = canvases.value[i].images[0];
        if (resource.service) {
          options.value.tileSources.push(
            `${resource.service["@id"]}/info.json`,
          );
        } else {
          options.value.tileSources.push(resource["@id"]);
        }
      }
    };

    const isManifest = (manifest) => {
      return manifest && Array.isArray(manifest.sequences);
    };

    onMounted(() => {
      fetchManifest();
    });

    return {
      ViewerToolbar,
    };
  },
});
</script>

<style src="./styles.css" lang="css"></style>
