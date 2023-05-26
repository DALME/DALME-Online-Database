import { filter, keys, map } from "ramda";

export const getColumns = (columnMap) => {
  const toColumn = (key) => ({
    align: columnMap[key].align,
    field: key,
    label: columnMap[key].label,
    name: key,
    sortable: columnMap[key].sortable,
    sortOrder: columnMap[key].sortOrder,
    classes: columnMap[key].classes,
    headerClasses: columnMap[key].headerClasses,
  });
  return map(toColumn, keys(columnMap));
};

export const getDefaults = (columnMap) => {
  let vCols = Object.keys(
    filter((column) => column.isDefaultVisible, columnMap),
  );
  let sortCol = Object.keys(
    filter((column) => column.isSortDefault, columnMap),
  )[0];
  let isSortDesc = columnMap[sortCol]["sortOrder"] === "da";

  return {
    sortBy: sortCol,
    sortDesc: isSortDesc,
    visibleColumns: vCols,
  };
};
