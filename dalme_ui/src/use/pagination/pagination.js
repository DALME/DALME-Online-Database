import S from "string";
import { equals, isNil } from "ramda";
import { computed, ref, unref, watch } from "vue";
import { storeToRefs } from "pinia";
import { usePrefStore } from "@/stores/preferences";

const transformField = (field) => S(field).underscore().s;

export const usePagination = (fetchData, listName, defaults) => {
  const $prefStore = usePrefStore();
  const { lists } = storeToRefs($prefStore);

  if (isNil(lists.value[listName])) {
    lists.value[listName] = {
      rowsPerPage: 20,
      visibleColumns: defaults.visibleColumns,
      sortBy: defaults.sortBy,
      sortDesc: defaults.sortDesc,
    };
  }

  const visibleColumns = ref(lists.value[listName]["visibleColumns"]);

  const defaultPagination = {
    descending: lists.value[listName]["sortDesc"],
    page: 1,
    rowsNumber: 0,
    rowsTotal: 0,
    rowsPerPage: lists.value[listName]["rowsPerPage"],
    sortBy: lists.value[listName]["sortBy"],
  };

  const pagination = ref(defaultPagination);

  const filter = ref("");

  const query = computed(() => {
    const pageData = unref(pagination);
    const params = new URLSearchParams();

    if (pageData.sortBy) {
      const ordering = transformField(pageData.sortBy);
      params.append("ordering", `${pageData.descending ? "-" : ""}${ordering}`);
    }
    if (filter.value) {
      params.append("search", filter.value);
    }

    const paging = {
      start: (pageData.page - 1) * pageData.rowsPerPage,
      length:
        pageData.rowsPerPage === 0 ? pageData.rowsNumber : pageData.rowsPerPage,
    };
    params.append("data", JSON.stringify(paging));

    return params.toString();
  });

  const onRequest = async (event) => {
    filter.value = event.filter;
    pagination.value = event.pagination;
  };

  // Provide a callback to the component in case it's necessary to call the
  // pagination-aware fetchData function from a watcher or something similar.
  const fetchDataPaginated = async () => fetchData(query.value);

  const resetPagination = () => (pagination.value = defaultPagination);

  const onChangeFilter = (value) => {
    filter.value = value;
    fetchDataPaginated();
  };

  const onChangePage = (value) => {
    pagination.value.page = value;
    fetchDataPaginated();
  };

  const onChangeRowsPerPage = (value) => {
    pagination.value.rowsPerPage = value;
    fetchDataPaginated();
  };

  watch(
    () => pagination.value,
    async (_, prev) => {
      if (prev) {
        await fetchDataPaginated();
      }
    },
    { immediate: true },
  );

  watch(
    [
      visibleColumns,
      () => pagination.value.rowsPerPage,
      () => pagination.value.sortBy,
      () => pagination.value.sortDesc,
    ],
    () => {
      if (
        !equals(lists.value[listName]["visibleColumns"], visibleColumns.value)
      ) {
        lists.value[listName]["visibleColumns"] = visibleColumns.value;
      }

      if (
        pagination.value.rowsPerPage !== lists.value[listName]["rowsPerPage"]
      ) {
        lists.value[listName]["rowsPerPage"] = pagination.value.rowsPerPage;
      }

      if (pagination.value.sortBy !== lists.value[listName]["sortBy"]) {
        lists.value[listName]["sortBy"] = pagination.value.sortBy;
      }

      if (pagination.value.sortDesc !== lists.value[listName]["sortDesc"]) {
        lists.value[listName]["sortDesc"] = pagination.value.sortDesc;
      }
    },
  );

  return {
    fetchDataPaginated,
    filter,
    onChangeFilter,
    onChangePage,
    onChangeRowsPerPage,
    onRequest,
    pagination,
    query,
    resetPagination,
    visibleColumns,
  };
};
