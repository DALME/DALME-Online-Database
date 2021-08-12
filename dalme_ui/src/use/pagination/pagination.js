import { inject, provide } from "vue";

const PaginationSymbol = Symbol();

// // https://quasar.dev/vue-components/table#server-side-pagination-filter-and-sorting
// const pagination = ref({
//   sortBy: 'desc',
//   descending: false,
//   page: 1,
//   rowsPerPage: 25,
//   rowsNumber: 10,
// })

// fetchFromServer

// const onRequest = () => {
//   const { page, rowsPerPage, sortBy, descending } = props.pagination;
//   const filter = props.filter;

//   loading.value = true;

//   // update rowsCount with appropriate value
//   pagination.value.rowsNumber = getRowsNumberCount(filter);

//   // get all rows if "All" (0) is selected
//   // TODO: We prob don't want "All" in these cases, too much load.
//   // TODO: Put in a max, eg 100 rows
//   const fetchCount =
//     rowsPerPage === 0 ? pagination.value.rowsNumber : rowsPerPage;

//   // calculate starting row of data
//   const startRow = (page - 1) * rowsPerPage;

//   // fetch data from "server"
//   const returnedData = fetchFromServer(
//     startRow,
//     fetchCount,
//     filter,
//     sortBy,
//     descending,
//   );

//   // clear out existing data and add new
//   rows.value.splice(0, rows.value.length, ...returnedData);

//   // don't forget to update local pagination object
//   pagination.value.page = page;
//   pagination.value.rowsPerPage = rowsPerPage;
//   pagination.value.sortBy = sortBy;
//   pagination.value.descending = descending;

//   loading.value = false;
// };

const pagination = () => null;

export const providePagination = () => provide(PaginationSymbol, pagination);

export const usePagination = () => inject(PaginationSymbol);
