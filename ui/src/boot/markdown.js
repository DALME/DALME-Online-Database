import { boot } from "quasar/wrappers";
import Plugin from "quasar-ui-qmarkdown-v2";
import "quasar-ui-qmarkdown-v2/dist/index.css";

export default boot(({ app }) => {
  app.use(Plugin);
});
