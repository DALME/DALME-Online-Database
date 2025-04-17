<template>
  <div class="map-container">
    <ol-map ref="map" class="map-box">
      <ol-view :center="centre" :zoom="zoom" :projection="projection" />
      <ol-tile-layer>
        <ol-source-xyz
          :url="baseTiles.url"
          :attributions="baseTiles.attributions"
          :max-zoom="baseTiles.maxZoom"
        />
      </ol-tile-layer>
      <ol-tile-layer>
        <ol-source-xyz
          v-if="showLabels"
          :url="labelTiles.url"
          :attributions="labelTiles.attributions"
          :max-zoom="labelTiles.maxZoom"
          :zDirection="labelTiles.zDirection"
        />
      </ol-tile-layer>
      <ol-vector-layer declutter="true">
        <ol-source-vector>
          <template v-for="(pt, idx) in points" :key="idx">
            <ol-feature>
              <ol-geom-point :coordinates="pt.coordinates" />
              <ol-style>
                <ol-style-circle :radius="radius">
                  <ol-style-fill :color="fill" />
                  <ol-style-stroke :color="stroke" :width="strokeWidth" />
                </ol-style-circle>
                <ol-style-text
                  v-if="pt.label"
                  :text="pt.label"
                  :offset-y="20"
                  font="700 14px 'Noto Sans', sans-serif"
                  declutter-mode="obstacle"
                />
              </ol-style>
            </ol-feature>
          </template>
        </ol-source-vector>
      </ol-vector-layer>
    </ol-map>
  </div>
</template>

<script>
import { defineComponent, onBeforeMount, onMounted, ref, useTemplateRef } from "vue";
import proj4 from "proj4";

export default defineComponent({
  name: "MapWidget",
  props: {
    places: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const map = useTemplateRef("map");
    const projection = "EPSG:3857";
    const radius = ref(7);
    const strokeWidth = ref(2);
    const fill = ref("#ff0000");
    const stroke = ref("#ffffff");
    const zoom = ref(8);
    const centre = ref([0, 0]);
    const points = ref([]);
    const view = ref(null);
    const extent = ref([]);
    const multiPoint = ref(false);
    const showLabels = ref(false);

    const baseTiles = {
      url: "https://{a-d}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
      attributions:
        // eslint-disable-next-line quotes
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      maxZoom: 19,
    };

    const labelTiles = {
      url: "https://{a-d}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png",
      attributions:
        // eslint-disable-next-line quotes
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      maxZoom: 19,
      zDirection: 200,
    };

    const convertCoordinates = (lon, lat) => {
      return proj4("EPSG:4326", "EPSG:3857", [parseFloat(lon), parseFloat(lat)]);
    };

    onBeforeMount(() => {
      for (const place of props.places) {
        if ("latitude" in place && "longitude" in place) {
          points.value.push({
            label:
              place.name === place.locationName
                ? place.name
                : `${place.name} (${place.locationName})`,
            coordinates: convertCoordinates(place.longitude, place.latitude),
          });
        }
      }

      if (points.value.length == 1) {
        centre.value = points.value[0].coordinates;
      } else {
        multiPoint.value = true;
        const ew = points.value.map((pt) => pt.coordinates[0]);
        const ns = points.value.map((pt) => pt.coordinates[1]);
        extent.value = [Math.min(...ew), Math.min(...ns), Math.max(...ew), Math.max(...ns)];
        centre.value = [
          (Math.max(...ew) + Math.min(...ew)) / 2,
          (Math.max(...ns) + Math.min(...ns)) / 2,
        ];
      }
    });

    onMounted(() => {
      view.value = map.value.map.getView();
      if (multiPoint.value) {
        view.value.fit(extent.value, { padding: [100, 100, 100, 100] });
      }
    });

    return {
      radius,
      fill,
      stroke,
      strokeWidth,
      centre,
      zoom,
      projection,
      points,
      baseTiles,
      labelTiles,
      showLabels,
    };
  },
});
</script>

<style lang="scss" scoped>
.map-container {
  padding: 5px;
}
.map-box {
  height: 400px;
  width: 100%;
  border: 1px solid #d1d1d1;
}
</style>
