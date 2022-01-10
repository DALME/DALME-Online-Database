import {
  any,
  isEmpty,
  isNil,
  map as rMap,
  mapObjIndexed,
  omit,
  keys,
  values,
} from "ramda";
import { computed, inject, provide, watch } from "vue";
import { onBeforeRouteLeave } from "vue-router";
import { assign, createMachine, spawn } from "xstate";
import { useMachine } from "@xstate/vue";

const MAX_FORMS = 5;
const EditingSymbol = Symbol();

export const provideEditing = () => {
  const createFormMachine = (cuid, kind, mode) =>
    createMachine(
      {
        id: cuid,
        initial: "editing",
        context: {
          kind,
          mode,
          dirty: false,
          validated: true,
          visible: true,
        },
        on: {
          SAVE: { target: "saving" },
          HIDE: { actions: "hide", internal: true },
          SHOW: { actions: "show", internal: true },
        },
        states: {
          editing: {},
          saving: {
            on: {
              RESOLVE: { target: "success" },
              REJECT: { target: "failure" },
            },
          },
          success: {
            entry: ["notifySuccess"],
            // TODO: Destroy or not? Set dirty to false.
          },
          failure: {
            entry: ["notifyFailure"],
            always: [{ target: "editing" }],
          },
        },
      },
      {
        actions: {
          hide: assign({ visible: false }),
          show: assign({ visible: true }),
          // TODO: Get the $notifier in here.
          notifyFailure: (_, event) => console.error(event.message),
          notifySuccess: (_, event) => console.error(event.message),
        },
      },
    );

  const createInlineMachine = () =>
    createMachine(
      {
        id: "inline",
        initial: "editing",
        on: {
          SAVE: { target: "saving" },
        },
        states: {
          editing: {},
          saving: {
            on: {
              RESOLVE: { target: "success" },
              REJECT: { target: "failure" },
            },
          },
          success: {
            entry: ["notifySuccess"],
          },
          failure: {
            entry: ["notifyFailure"],
          },
        },
      },
      {
        actions: {
          // TODO: $notifier.CRUD.inlineUpdateSuccess(event.message);
          notifyFailure: (_, event) => console.error(event.message),
          // TODO: $notifier.CRUD.inlineUpdateFailed(event.message);
          notifySuccess: (_, event) => console.error(event.message),
        },
      },
    );

  const editingMachine = createMachine(
    {
      id: "editing",
      initial: "normal",
      context: {
        detail: false,
        focus: null, // focus : null || "inline" || cuid
        forms: {},
        inline: null,
        maxForms: MAX_FORMS,
      },
      on: {
        DESTROY_FORM: { target: "destroyForm" },
        DESTROY_INLINE: { target: "destroyInline" },
        SET_DETAIL: { actions: "setDetail", internal: true },
        SET_FOCUS: { actions: "setFocus", internal: true },
        SPAWN_FORM: {
          target: "editing",
          actions: "spawnForm",
          cond: "canSpawn",
        },
        SPAWN_INLINE: {
          target: "editing",
          actions: "spawnInline",
          cond: "noInline",
        },
        RESET: { target: "reset" },
      },
      states: {
        normal: {},
        editing: {},
        destroyForm: {
          entry: ["gcForm"],
          always: [
            { target: "editing", cond: "hasForms" },
            { target: "normal" },
          ],
        },
        destroyInline: {
          entry: ["gcInline"],
          always: [
            { target: "editing", cond: "hasForms" },
            { target: "normal" },
          ],
        },
        reset: {
          entry: ["gcForms"],
          always: [{ target: "normal" }],
        },
      },
    },
    {
      actions: {
        spawnInline: assign({
          focus: "inline",
          inline: spawn(createInlineMachine()),
        }),
        spawnForm: assign({
          focus: (_, event) => event.cuid,
          forms: (context, event) => {
            return {
              [event.cuid]: spawn(
                createFormMachine(event.cuid, event.kind, event.mode),
              ),
              ...context.forms,
            };
          },
        }),
        gcInline: assign({
          focus: (context, _) =>
            context.focus === "inline" ? null : context.focus,
          inline: null,
        }),
        gcForm: assign({
          focus: (context, event) =>
            context.focus === event.cuid ? null : context.focus,
          forms: (context, event) => {
            context.forms[event.cuid].stop();
            return omit([event.cuid], context.forms);
          },
        }),
        gcForms: assign({
          forms: (context) => {
            rMap((actor) => actor.stop(), values(context.forms));
            return {};
          },
        }),
        setDetail: assign({
          detail: (_, event) => event.value,
        }),
        setFocus: assign({
          focus: (_, event) => event.value,
        }),
      },
      guards: {
        canSpawn: (context) => keys(context.forms).length < context.maxForms,
        hasForms: (context) => keys(context.forms).length > 0,
        noInline: (context) => isNil(context.inline),
      },
    },
  );

  // Main interface.
  const machine = useMachine(editingMachine);

  // Convenience getters lensing into the machine context.
  const focus = computed(() => machine.state.value.context.focus);
  const forms = computed(() => machine.state.value.context.forms);
  const inline = computed(() => machine.state.value.context.inline);

  // Helper functions.
  const hideAll = () => {
    for (let actor of values(forms.value)) {
      actor.send("HIDE");
    }
  };
  const showAll = () => {
    for (let actor of values(forms.value)) {
      actor.send("SHOW");
    }
  };

  // Track the actual actor object that is under focus.
  const focusActor = computed(() => {
    const value = machine.state.value.context.focus;
    if (isNil(value)) return null;
    return value === "inline"
      ? machine.state.value.context.inline
      : machine.state.value.context.forms[value];
  });

  // Tell us if any actors are in their 'saving' state.
  const submitting = computed(() => {
    const formsSaving = rMap(
      (actor) => actor.getSnapshot().matches("saving"),
      values(forms.value),
    );
    const inlineSaving =
      !isNil(inline.value) && inline.value.getSnapshot().matches("saving");
    const isSaving = [...formsSaving, inlineSaving];
    return any((saving) => saving === true, isSaving);
  });

  // If there's absolutely nothing valid from the global POV, if we're in the
  // middle of an API call, we can use this to disable the submit button.
  const disabled = computed(() => {
    const validated = mapObjIndexed(
      (actor) => actor.getSnapshot().context.validated,
      forms.value,
    );
    const nothingValid =
      isNil(inline.value) &&
      (isEmpty(validated) ||
        !any((value) => value === true, values(validated)));
    const focusValid =
      inline.value || (focusActor.value && validated[focus.value]);
    return nothingValid || !focusValid || submitting.value;
  });

  // Invokes a particular form's submit callback whenever its actor transitions
  // to the "saving" state.
  const formSubmitWatcher = (actorState, handleSubmit) => {
    watch(
      () => actorState.value,
      async (newActorState) => {
        if (newActorState.matches("saving")) {
          await handleSubmit();
        }
      },
    );
  };

  // TODO: Call on all detail pages.
  const editingDetailRouteGuard = () => {
    machine.send("SET_DETAIL", { value: true });
    onBeforeRouteLeave(() => machine.send("SET_DETAIL", { value: false }));
  };

  provide(EditingSymbol, {
    disabled,
    editingDetailRouteGuard,
    formSubmitWatcher,
    focus,
    focusActor,
    forms,
    hideAll,
    inline,
    machine,
    showAll,
    submitting,
  });
};

export const useEditing = () => inject(EditingSymbol);
