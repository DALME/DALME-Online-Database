import { useConstants } from "@/use";
import { filterItemClass, filterItemClassSelected, userFetcher } from "@/components";

const { ticketTagColours } = useConstants();

const tags = Object.keys(ticketTagColours).map((tag) => ({
  label: tag,
  value: tag,
  class: "text-grey-8",
  classSelected: "text-weight-bold bg-indigo-1 text-indigo-5",
  icon: {
    name: "circle",
    color: ticketTagColours[tag]["text"],
    size: "xs",
  },
}));

export const filterList = (userId) => ({
  preset: [
    {
      field: "status",
      value: 0,
      label: "Open issues",
      isolation: false,
    },
    {
      field: "status",
      value: 1,
      label: "Closed issues",
      isolation: false,
    },
    {
      field: "creation_user",
      value: userId,
      label: "Your issues",
      isolation: false,
    },
    {
      field: "assigned_to",
      value: userId,
      label: "Assigned to you",
      isolation: false,
    },
  ],
  filters: [
    {
      label: "Tags",
      selection: "multiple",
      type: "generic",
      field: "tags",
      items: tags,
      isolation: false,
    },
    {
      label: "Author",
      selection: "single",
      type: "users",
      field: "creation_user",
      fetcher: userFetcher,
      returnField: "id",
      showSelected: true,
      searchable: true,
      isolation: false,
      class: filterItemClass,
      classSelected: filterItemClassSelected,
    },
    {
      label: "Assignee",
      selection: "single",
      type: "users",
      field: "assigned_to",
      fetcher: userFetcher,
      returnField: "id",
      showSelected: true,
      searchable: true,
      isolation: false,
      class: filterItemClass,
      classSelected: filterItemClassSelected,
    },
  ],
});

export const sortList = () => [
  {
    label: "Newest",
    value: {
      column: "creation_timestamp",
      desc: true,
    },
  },
  {
    label: "Oldest",
    value: {
      column: "creation_timestamp",
      desc: false,
    },
  },
  {
    label: "Most commented",
    value: {
      column: "comment_count",
      desc: true,
    },
  },
  {
    label: "Least commented",
    value: {
      column: "comment_count",
      desc: false,
    },
  },
  {
    label: "Recently updated",
    value: {
      column: "modification_timestamp",
      desc: true,
    },
  },
  {
    label: "Least recently updated",
    value: {
      column: "modification_timestamp",
      desc: false,
    },
  },
];
