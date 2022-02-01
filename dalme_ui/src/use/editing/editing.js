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
import { computed, inject, provide, ref, watch } from "vue";
import { onBeforeRouteLeave } from "vue-router";
import { assign, createMachine, send, spawn } from "xstate";
import { useMachine, useSelector } from "@xstate/vue";

import { default as notifier } from "@/notifier";

const MAX_FORMS = 5;
const EditingSymbol = Symbol();

export const provideEditing = () => {
  const createFormMachine = (cuid, kind, mode, initialData) =>
    createMachine(
      {
        id: cuid,
        initial: "editing",
        context: {
          kind,
          mode,
          initialData,
          validated: false, // TODO: Switch to false when formvuelate issue resolved.
          visible: true,
        },
        on: {
          SAVE: { target: "saving" },
          HIDE: { actions: "hide", internal: true },
          SHOW: { actions: "show", internal: true },
          VALIDATE: { actions: "validate", internal: true },
        },
        states: {
          editing: {},
          saving: {
            on: {
              // TODO: respond({ type: 'SUCCESS', message: 'Bla' }, { delay: 10 })
              // The SAVE must come from the editingMachine, which it does...
              RESOLVE: { actions: "notifySuccess", target: "complete" },
              REJECT: { actions: "notifyFailure", target: "editing" },
            },
          },
          complete: {
            type: "final",
          },
        },
      },
      {
        actions: {
          hide: assign({ visible: false }),
          show: assign({ visible: true }),
          notifyFailure: (context) =>
            notifier.CRUD.failure(`Could not create ${context.kind}`),
          notifySuccess: (context) =>
            notifier.CRUD.success(`${context.kind} created`),
          validate: assign({
            validated: (_, event) => (event.validated ? true : false),
          }),
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
              RESOLVE: { actions: "notifySuccess", target: "complete" },
              REJECT: { actions: "notifyFailure", target: "editing" },
            },
          },
          complete: {
            type: "final", // No need for gc, done in Table.vue itself.
          },
        },
      },
      {
        actions: {
          debug: () => {},
          notifyFailure: () =>
            notifier.CRUD.failure("Couldn't save inline edits"),
          notifySuccess: () => notifier.CRUD.success("Inline edits saved"),
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
        forms: {}, // forms : { cuid: actor }
        inline: null, // inline : null || actor
        maxForms: MAX_FORMS,
      },
      on: {
        DESTROY_FORM: { target: "destroyForm" },
        DESTROY_INLINE: { target: "destroyInline" },
        RESET: { target: "reset" },
        SAVE_FOCUS: { actions: "saveFocus", internal: true },
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
        gcInline: assign({
          focus: (context) =>
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
        saveFocus: send(
          { type: "SAVE" },
          {
            to: (context) =>
              context.focus === "inline"
                ? context.inline
                : context.forms[context.focus],
          },
        ),
        spawnInline: assign({
          focus: "inline",
          inline: () => spawn(createInlineMachine()),
        }),
        spawnForm: assign({
          focus: (_, event) => event.cuid,
          forms: (context, event) => {
            return {
              [event.cuid]: spawn(
                createFormMachine(
                  event.cuid,
                  event.kind,
                  event.mode,
                  event.initialData,
                ),
              ),
              ...context.forms,
            };
          },
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
  const { service } = machine;

  // Convenience getters lensing into the machine context.
  const focus = useSelector(service, (state) => state.context.focus);
  const forms = useSelector(service, (state) => state.context.forms);
  const inline = useSelector(service, (state) => state.context.inline);
  const isDetail = useSelector(service, (state) => state.context.detail);

  const mouseoverSubmit = ref(false);

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

  // If there's absolutely nothing valid from the global POV, or if we're in
  // the middle of an API call, we can use this to disable the submit button.
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
      focus.value === "inline" || (focusActor.value && validated[focus.value]);
    return nothingValid || !focusValid || submitting.value;
  });

  const afterEditingRefresh = ref("false");

  // Invokes a particular form's submit callback whenever its actor transitions
  // to the "saving" state.
  const formSubmitWatcher = (actor, handleSubmit) =>
    watch(
      () => actor.value,
      async (newActor) => {
        if (newActor.value === "saving") {
          await handleSubmit();
          afterEditingRefresh.value = true;
        }
      },
    );

  // Make sure any relevant data is refreshed when a form is submitted. This
  // watcher needs to be instantiated on any page that might need to rerender
  // as a side-effect after some, unspecified CRUD operation occurs that it has
  // no precise knowledge of. Not the most satisfying thing to have to do but
  // probably the simplest for our 'free-floating' editing patterns.
  const afterEditingRefreshWatcher = (fetchData) =>
    watch(
      () => afterEditingRefresh.value,
      async (newValue, oldValue) => {
        if (oldValue === false && newValue === true) {
          await fetchData();
          if (afterEditingRefresh.value === true) {
            afterEditingRefresh.value = false;
          }
        }
      },
    );

  const editingDetailRouteGuard = () => {
    machine.send("SET_DETAIL", { value: true });
    onBeforeRouteLeave(() => {
      machine.send("SET_DETAIL", { value: false });
    });
  };

  provide(EditingSymbol, {
    afterEditingRefreshWatcher,
    disabled,
    editingDetailRouteGuard,
    formSubmitWatcher,
    focus,
    focusActor,
    forms,
    hideAll,
    inline,
    isDetail,
    machine,
    mouseoverSubmit,
    showAll,
    submitting,
  });
};

export const useEditing = () => inject(EditingSymbol);
