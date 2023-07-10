import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { API as apiInterface, requests } from "@/api";
import { filter as rFilter, groupBy, forEachObjIndexed } from "ramda";
import { useAuthStore } from "@/stores/auth";
import { taskListsSchema } from "@/schemas";

export const useTasklistStore = defineStore("tasklistStore", () => {
  // stores
  const auth = useAuthStore();

  // state
  const value = ref([]);
  const timestamp = ref(null);
  const loading = ref(false);

  // getters
  const _isStale = computed(() => Date.now() - timestamp.value > 86400000);
  const isLoaded = computed(() => value.value.length);
  const grouped = computed(() => groupBy((list) => list.teamLink.name, value.value));
  const index = computed(() =>
    forEachObjIndexed((value, key, obj) => {
      obj[key] = Array.from(value, (val) => val.name);
    }, grouped.value),
  );

  // actions
  const $reset = () => {
    value.value = [];
    timestamp.value = null;
    loading.value = false;
  };

  const init = () => {
    $reset();
    fetchData(getRequest("user", 50)).then((response) => {
      value.value = response;
      loading.value = false;
    });
  };

  const getRequest = (type, limit, offset = 0, query = null) => {
    if (type == "user") return requests.tasks.getUserTasklists(auth.userId);
    return requests.tasks.getTasklists(query, limit, offset);
  };

  const fetchData = (request) => {
    return new Promise((resolve) => {
      const { success, data, fetchAPI } = apiInterface();
      loading.value = true;
      fetchAPI(request).then(() => {
        if (success.value) {
          taskListsSchema.validate(data.value.data, { stripUnknown: true }).then((response) => {
            timestamp.value = Date.now();
            return resolve(response);
          });
        }
      });
    });
  };

  const getList = (id) => {
    return rFilter((x) => x.id == id, value.value)[0];
  };

  return {
    value,
    timestamp,
    loading,
    isLoaded,
    $reset,
    init,
    getRequest,
    fetchData,
    getList,
    grouped,
    index,
  };
});
