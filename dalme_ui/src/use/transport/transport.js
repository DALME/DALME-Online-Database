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
import { computed, inject, provide, watch } from "vue";

const TransportSymbol = Symbol();

export const provideTransport = (transport, tracked) => {
  const dirty = computed(() => {
    return transport.history.value.map((entry) => ({
      id: entry.snapshot.id,
      field: entry.snapshot.field,
    }));
  });
  const isDirty = computed(() => dirty.value.length > 1);
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
  };

  const transportWatcher = (rows) => {
    watch(
      () => transport.history.value,
      (diffs, prevDiffs) => {
        const undone = diffs.length < prevDiffs.length;
        const diff = undone ? prevDiffs[0].snapshot : diffs[0].snapshot;
        // TODO: Check to see if prevValue was an object, merge with that.
        // Although, need to consider the FK situation generally.
        // Setup all the fields with validation.
        // But setup fk choices on country if having time.
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
