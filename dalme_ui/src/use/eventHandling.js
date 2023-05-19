import { EventBus } from "quasar";
import { inject, provide } from "vue";
import notifier from "@/notifier";

const EventHandlingSymbol = Symbol();

export const provideEventHandling = () => {
  const eventBus = new EventBus();

  const onError = (evt) => {
    console.log(evt);
    // const { message, filename, lineno, colno, error } = evt;
    // const response = error.response;
    // if (response && response.status >= 400 && response.status < 405) {
    //   // You can handle this differently
    //   sentryLogEngine(error);
    //   return false;
    // }
    // evt.preventDefault().stopImmediatePropagation();
    displayErrorAlert("error-errorHandler triggered", evt);
    return false;
    // showInConsole(message, filename, lineno, colno, error);
  };

  const onRenderError = (err, instance, info) => {
    console.log("rendererror-errorHandler triggered", err);
    // displayErrorAlert("rendererror-errorHandler triggered", err);
    return false;
    // console.log("RenderError", err, instance, info);
  };

  const onRenderWarning = (msg, instance, trace) => {
    displayErrorAlert("warning-errorHandler triggered");
    return false;
    // console.log("RenderError", msg, instance, trace);
  };

  const initEventHandler = () => {
    console.log("starting error handler");
    window.addEventListener("error", onError, { capture: true });
  };

  const showInConsole = (message, filename, lineno, colno, error) => {
    console.log(message, filename, lineno, colno, error);
  };

  const displayErrorAlert = (message) => {
    console.log(message);
    // Notify.create({
    //   color: "red",
    //   message: message,
    //   position: "top-right",
    //   icon: "speaker_notes",
    // });
  };

  provide(EventHandlingSymbol, {
    notifier,
    eventBus,
    onError,
    displayErrorAlert,
  });

  return { onError, initEventHandler, onRenderError };
};

export const useEventHandling = () => inject(EventHandlingSymbol);
