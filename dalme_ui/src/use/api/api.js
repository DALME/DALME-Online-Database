import { API } from "@/api";

// We don't use provide/inject here because we want to return a new closure of
// values each time we instantiate API in order to track the results of our
// remote requests. Injecting it on the route works for singleton values like
// the store but it will result in race conditions and false positives when
// rendering a tree making more than one API request during the same render.
export const useAPI = (context) => API(context);
