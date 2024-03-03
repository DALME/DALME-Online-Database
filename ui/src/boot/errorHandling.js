import { boot } from "quasar/wrappers";
import { provideErrorHandling } from "@/use";

export default boot(({ app }) => {
  const { onRenderError, onRenderWarning } = provideErrorHandling();
  app.config.errorHandler = (err, instance, info) => {
    // the error, the component instance that triggered the error,
    // and an information string specifying the error source type
    onRenderError(err, instance, info);
  };

  app.config.warnHandler = (msg, instance, trace) => {
    onRenderWarning(msg, instance, trace);
  };
});
