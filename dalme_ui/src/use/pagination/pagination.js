import { computed, ref, unref, watch } from "vue";

export const usePagination = (fetchData) => {
  const filter = ref("");

  const pagination = ref({
    descending: false,
    page: 1,
    rowsNumber: null,
    rowsPerPage: 10,
    sortBy: null,
  });

  const query = computed(() => {
    const pageData = unref(pagination);
    const params = new URLSearchParams();

    if (pageData.sortBy) {
      params.append(
        "ordering",
        `${pageData.descending ? "-" : ""}${pageData.sortBy}`,
      );
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

  watch(
    () => pagination.value,
    async () => {
      await fetchData(query.value);
    },
    { immediate: true },
  );

  return { filter, pagination, onRequest };
};
