import { EventBus, Notify } from "quasar";
import { inject, provide } from "vue";
import notifier from "@/notifier";

const EventHandlingSymbol = Symbol();

export const provideEventHandling = () => {
  const eventBus = new EventBus();

  const onError = (evt) => {
    evt.preventDefault().stopImmediatePropagation();
    displayErrorAlert("error-errorHandler triggered", evt);
    // showInConsole(message, filename, lineno, colno, error);
    return false;
  };

  const onRenderError = (err, instance, info) => {
    displayErrorAlert("rendererror-errorHandler triggered", err);
    console.log("rendererror-errorHandler triggered", err, instance, info);
    return false;
  };

  const initEventHandler = () => {
    console.log("starting error handler");
    window.addEventListener("error", onError, { capture: true });
  };

  const displayErrorAlert = (message) => {
    Notify.create({
      color: "red",
      message: message,
      position: "top-right",
      icon: "speaker_notes",
    });
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
