import S from "string";
import { computed, ref, unref, watch } from "vue";

const transformField = (field) => {
  const transformMap = { objId: "id" };
  const value = transformMap[field] || field;
  return S(value).underscore().s;
};

export const usePagination = (fetchData) => {
  const defaultPagination = {
    descending: false,
    page: 1,
    rowsNumber: null,
    rowsPerPage: 10,
    sortBy: null,
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

  watch(
    () => pagination.value,
    async (_, prev) => {
      if (prev) {
        await fetchDataPaginated();
      }
    },
    { immediate: true },
  );

  return {
    fetchDataPaginated,
    filter,
    onRequest,
    pagination,
    query,
    resetPagination,
  };
};
