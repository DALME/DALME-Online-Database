import { boot } from "quasar/wrappers";
import OpenLayersMap from "vue3-openlayers";
import "vue3-openlayers/styles.css";

export default boot(({ app }) => {
  app.use(OpenLayersMap);
});
