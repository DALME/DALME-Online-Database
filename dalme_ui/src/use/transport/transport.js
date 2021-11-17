import {
  findIndex,
  groupBy,
  head,
  includes,
  lensProp,
  map,
  prop,
  propEq,
  set,
} from "ramda";
import { computed, inject, provide, ref, watch } from "vue";

const TransportSymbol = Symbol();

export const provideTransport = (transport, tracked) => {
  const dirty = computed(() => {
    return transport.history.value.slice(0, -1).map((entry) => ({
      id: entry.snapshot.id,
      field: entry.snapshot.field,
    }));
  });
  const isDirty = computed(() => dirty.value.length > 0);
  const cellIsDirty = (id, field) => includes({ id, field }, dirty.value);

  const onDiff = (id, field, val, prev) => {
    tracked.value = { id, field, new: val, old: prev };
    transport.commit();
  };

  const objDiffs = computed(() => {
    const snapshots = transport.history.value
      .map((diff) => diff.snapshot)
      .slice(0, -1);
    const byId = groupBy(prop("id"))(snapshots);
    const byField = map((diffs) => groupBy(prop("field"))(diffs), byId);
    const values = map(
      (diffs) => map((history) => head(history).new, diffs),
      byField,
    );
    return values;
  });

  const resetTransport = () => {
    transport.clear();
    tracked.value = ref({ id: null, field: null, new: null, old: null });
  };

  const transportWatcher = (rows) => {
    watch(
      () => transport.history.value,
      (diffs, prevDiffs) => {
        const undone = diffs.length < prevDiffs.length;
        const diff = undone ? prevDiffs[0].snapshot : diffs[0].snapshot;
        // TODO: Check to see if prevValue was an object, merge with that.
        // Although, we need to consider the FK situation generally.
        const value = undone ? diff.old : diff.new;
        const lens = lensProp(diff.field);
        const rowIndex = findIndex(propEq("id", diff.id))(rows.value);
        const updated = set(lens, value, rows.value[rowIndex]);
        rows.value.splice(rowIndex, 1, updated);
      },
    );
  };

  provide(TransportSymbol, {
    onDiff,
    isDirty,
    objDiffs,
    cellIsDirty,
    resetTransport,
    transportWatcher,
  });
};

export const useTransport = () => inject(TransportSymbol);
