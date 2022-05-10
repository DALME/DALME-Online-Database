import {
  any,
  pipe,
  filter as rFilter,
  indexBy,
  isEmpty,
  isNil,
  map as rMap,
  omit,
  prop,
  keys,
  values,
} from "ramda";
import { computed, inject, provide, ref, watch } from "vue";
import { onBeforeRouteLeave } from "vue-router";
import { assign, createMachine, send, spawn } from "xstate";
import { useActor, useMachine, useSelector } from "@xstate/vue";

import { default as notifier } from "@/notifier";

const MAX_MODALS = 10;
const EditingSymbol = Symbol();

export const provideEditing = () => {
  const createFormMachine = (cuid, key, kind, mode, initialData) =>
    createMachine(
      {
        id: cuid,
        initial: "editing",
        context: {
          key,
          kind,
          mode,
          initialData,
          validated: false, // TODO: This should be a state!
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
            notifier.CRUD.failure(`Could not save ${context.kind}`),
          notifySuccess: (context) =>
            notifier.CRUD.success(`${context.kind} saved`),
          validate: assign({
            validated: (_, event) => (event.validated ? true : false),
          }),
        },
      },
    );

  const createFolioMachine = (cuid, key, metadata) =>
    createMachine(
      {
        id: cuid,
        initial: "render",
        context: { kind: "Folio", mode: "View", key, metadata, visible: true },
        on: {
          HIDE: { actions: "hide", internal: true },
          SHOW: { actions: "show", internal: true },
        },
        states: {
          render: {},
        },
      },
      {
        actions: {
          hide: assign({ visible: false }),
          show: assign({ visible: true }),
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
        modals: {}, // modals : { cuid: { kind: 'form' | 'folio', actor } }
        inline: null, // inline : null || actor
        maxModals: MAX_MODALS,
      },
      on: {
        DESTROY_MODAL: { target: "destroyModal" },
        DESTROY_INLINE: { target: "destroyInline" },
        RESET: { target: "reset" },
        SAVE_FOCUS: { actions: "saveFocus", internal: true, cond: "saveable" },
        SET_IS_DETAIL_PAGE: { actions: "setIsDetailPage", internal: true },
        SET_FOCUS: { actions: "setFocus", internal: true },
        SPAWN_FOLIO: {
          target: "editing",
          actions: "spawnFolio",
          cond: "canSpawn",
        },
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
        destroyModal: {
          entry: ["gcModal"],
          always: [
            { target: "editing", cond: "hasModals" },
            { target: "normal" },
          ],
        },
        destroyInline: {
          entry: ["gcInline"],
          always: [
            { target: "editing", cond: "hasModals" },
            { target: "normal" },
          ],
        },
        reset: {
          entry: ["gcModals"],
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
        gcModal: assign({
          focus: (context, event) =>
            context.focus === event.cuid ? null : context.focus,
          modals: (context, event) => {
            const { actor } = context.modals[event.cuid];
            actor.stop();
            return omit([event.cuid], context.modals);
          },
        }),
        gcModals: assign({
          modals: (context) => {
            rMap(({ actor }) => actor.stop(), values(context.modals));
            return {};
          },
        }),
        setIsDetailPage: assign({
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
                : context.modals[context.focus].actor,
          },
        ),
        spawnFolio: assign({
          focus: (_, event) => event.cuid,
          modals: (context, event) => {
            return {
              [event.cuid]: {
                kind: "folio",
                actor: spawn(
                  createFolioMachine(event.cuid, event.key, event.metadata),
                  { sync: true },
                ),
              },
              ...context.modals,
            };
          },
        }),
        spawnForm: assign({
          focus: (_, event) => event.cuid,
          modals: (context, event) => {
            return {
              [event.cuid]: {
                kind: "form",
                actor: spawn(
                  createFormMachine(
                    event.cuid,
                    event.key,
                    event.kind,
                    event.mode,
                    event.initialData,
                  ),
                  { sync: true },
                ),
              },
              ...context.modals,
            };
          },
        }),
        spawnInline: assign({
          focus: "inline",
          inline: () => spawn(createInlineMachine()),
        }),
      },
      guards: {
        saveable: (context) => {
          if (isNil(context.focus)) {
            return false;
          }
          if (context.focus === "inline") {
            return true;
          }
          return context.modals[context.focus].kind === "folio" ? true : false;
        },
        canSpawn: (context) => keys(context.modals).length < context.maxModals,
        hasModals: (context) => keys(context.modals).length > 0,
        noInline: (context) => isNil(context.inline),
      },
    },
  );

  // Main interface.
  const machine = useMachine(editingMachine);
  const { service } = machine;

  // Convenience getters lensing into the machine context.
  const focus = useSelector(service, (state) => state.context.focus);
  const modals = useSelector(service, (state) => state.context.modals);
  const folios = useSelector(service, (state) =>
    rFilter(({ kind }) => kind === "folio", state.context.modals),
  );
  const forms = useSelector(service, (state) =>
    rFilter(({ kind }) => kind === "form", state.context.modals),
  );
  const inline = useSelector(service, (state) => state.context.inline);
  const isDetail = useSelector(service, (state) => state.context.detail);

  // Reactive values.
  const mouseoverSubmit = ref(false);
  const recenter = ref(null);
  const hideEditing = ref(null);
  const showEditing = ref(null);

  // TODO: Need a way to broadcast or batch these sends or they could
  // (hypothetically) result in N (where N = keys(modals).length)
  // page re-renders as each actor transitions.
  const hideAll = () => {
    for (const { actor } of values(modals.value)) {
      const { send } = useActor(actor);
      send("HIDE");
    }
  };
  const showAll = () => {
    for (const { actor } of values(modals.value)) {
      const { send } = useActor(actor);
      send("SHOW");
    }
  };

  // An index of keys to cuids for identifying which objects are already open
  // in the window index and so preventing duplicates (we can refocus instead).
  const editingIndex = computed(() => {
    const process = pipe(
      rMap(({ actor }) => {
        return { cuid: actor.machine.id, key: actor.getSnapshot().context.key };
      }),
      indexBy(prop("key")),
    );
    return process([...values(forms.value), ...values(folios.value)]);
  });

  // Tell us if any form actors are in their 'saving' state.
  const submitting = computed(() => {
    const formsSaving = rMap(
      ({ actor }) => actor.getSnapshot().matches("saving"),
      values(forms.value),
    );

    const inlineSaving =
      !isNil(inline.value) && inline.value.getSnapshot().matches("saving");

    const isSaving = [...formsSaving, inlineSaving];

    // TODO: any(Boolean, isSaving);
    return any((saving) => Boolean(saving), isSaving);
  });

  // Close the editor when there's no CRUD happening.
  const noEditing = computed(
    () => isNil(inline.value) && isEmpty(modals.value),
  );
  watch(
    () => noEditing.value,
    (newValue) => {
      if (newValue) {
        hideEditing.value();
      }
    },
  );

  // Invokes a particular form's submit callback whenever its actor transitions
  // to the "saving" state.
  const formSubmitWatcher = (actor, handleSubmit) =>
    watch(
      () => actor.value,
      async (newActor) => {
        if (newActor.value === "saving") {
          await handleSubmit(postSubmitRefresh);
        }
      },
    );

  // Make sure any relevant data is refreshed when a form is submitted. This
  // watcher needs to be instantiated on any page that might need to rerender
  // as a side-effect after some, unspecified CRUD operation occurs that it has
  // no precise knowledge of. Not the most satisfying thing to have to do but
  // probably the simplest for our 'free-floating' editing patterns.
  const postSubmitRefresh = ref(false);
  const postSubmitRefreshWatcher = (fetchData) =>
    watch(
      () => postSubmitRefresh.value,
      async (newValue, oldValue) => {
        if (!oldValue && newValue) {
          await fetchData();
          postSubmitRefresh.value = false;
        }
      },
    );

  // Reposition a form in the middle of the viewport.
  const recenterWatcher = (cuid, x, y) =>
    watch(
      () => recenter.value,
      (newRecenter) => {
        if (!isNil(newRecenter) && newRecenter === cuid) {
          x.value = window.innerWidth / 3.75;
          y.value = window.innerHeight / 10;
          recenter.value = null;
        }
      },
    );

  // Inform the editing logic if we are on a detail page. This needs to be
  // manually instantiated in any detail page setup methods. NOTE: Could
  // preferably share a single, abstract DetailPage component at some point in
  // the refactored future and just call this there, once.
  const resource = ref(null);
  const editingDetailRouteGuard = () => {
    machine.send("SET_IS_DETAIL_PAGE", { value: true });
    onBeforeRouteLeave(() => {
      machine.send("SET_IS_DETAIL_PAGE", { value: false });
    });
  };

  provide(EditingSymbol, {
    editingDetailRouteGuard,
    editingIndex,
    hideEditing,
    folios,
    formSubmitWatcher,
    forms,
    focus,
    modals,
    hideAll,
    inline,
    isDetail,
    machine,
    mouseoverSubmit,
    postSubmitRefreshWatcher,
    recenter,
    recenterWatcher,
    resource,
    showAll,
    showEditing,
    submitting,
  });
};

export const useEditing = () => inject(EditingSymbol);
