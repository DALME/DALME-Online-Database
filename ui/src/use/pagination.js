import S from "string";
import { equals, isEmpty } from "ramda";
import { computed, ref, unref, watch } from "vue";
import { nully } from "@/utils";
import { useSettingsStore } from "@/stores/settings";

const transformField = (field) => S(field).underscore().s;

export const usePagination = (fetchData, listName, defaults, embedded = false) => {
  const settings = useSettingsStore();
  const lists = settings.preferences.listPreferences.value;

  if (nully(lists[listName])) {
    lists[listName] = {
      rowsPerPage: 20,
      visibleColumns: defaults.visibleColumns,
      sortBy: defaults.sortBy,
      sortDesc: defaults.sortDesc,
    };
  }

  const visibleColumns = ref(lists[listName]["visibleColumns"]);

  const defaultPagination = {
    descending: lists[listName]["sortDesc"],
    page: 1,
    rowsNumber: 0,
    rowsTotal: 0,
    rowsPerPage: embedded ? 5 : lists[listName]["rowsPerPage"],
    sortBy: lists[listName]["sortBy"],
  };

  const pagination = ref(defaultPagination);
  const search = ref("");
  const activeFilters = ref({});

  const query = computed(() => {
    const pageData = unref(pagination);
    const params = new URLSearchParams();

    if (pageData.sortBy) {
      const ordering = transformField(pageData.sortBy);
      params.append("ordering", `${pageData.descending ? "-" : ""}${ordering}`);
    }

    if (search.value) {
      params.append("search", search.value);
    }

    if (!isEmpty(activeFilters.value)) {
      for (const field in activeFilters.value) {
        params.append(field, activeFilters.value[field]);
      }
    }

    params.append("offset", (pageData.page - 1) * pageData.rowsPerPage);
    params.append("limit", pageData.rowsPerPage);

    return params.toString();
  });

  const onRequest = async (event) => {
    search.value = event.search;
    pagination.value = event.pagination;
  };

  // Provide a callback to the component in case it's necessary to call the
  // pagination-aware fetchData function from a watcher or something similar.
  const fetchDataPaginated = async () => fetchData(query.value);

  const resetPagination = () => (pagination.value = defaultPagination);

  const onChangeSearch = (value) => {
    search.value = value;
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

  const onChangeFilters = (filter) => {
    if (filter.field in activeFilters.value && activeFilters.value[filter.field] === filter.value) {
      delete activeFilters.value[filter.field];
    } else {
      activeFilters.value[filter.field] = filter.value;
    }
    fetchDataPaginated();
  };

  const onClearFilters = () => {
    activeFilters.value = [];
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
      if (!equals(lists[listName]["visibleColumns"], visibleColumns.value)) {
        lists[listName]["visibleColumns"] = visibleColumns.value;
      }

      if (pagination.value.rowsPerPage !== lists[listName]["rowsPerPage"]) {
        lists[listName]["rowsPerPage"] = pagination.value.rowsPerPage;
      }

      if (pagination.value.sortBy !== lists[listName]["sortBy"]) {
        lists[listName]["sortBy"] = pagination.value.sortBy;
      }

      if (pagination.value.sortDesc !== lists[listName]["sortDesc"]) {
        lists[listName]["sortDesc"] = pagination.value.sortDesc;
      }
    },
  );

  return {
    activeFilters,
    fetchDataPaginated,
    onChangeSearch,
    onChangePage,
    onChangeRowsPerPage,
    onChangeFilters,
    onClearFilters,
    onRequest,
    pagination,
    query,
    resetPagination,
    search,
    visibleColumns,
  };
};
