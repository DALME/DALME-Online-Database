import { requests } from "@/api";
import { OptionListSchema } from "@/schemas";
import { filterItemClass, filterItemClassSelected, optionFetcher, userFetcher } from "@/components";

const recordTypes = () =>
  optionFetcher(
    requests.attributeTypes.getAttributeTypeOptions("record_type", true),
    OptionListSchema,
  );

export const filterList = (userId) => ({
  preset: [
    {
      field: "owner",
      value: userId,
      label: "Your record groups",
      isolation: false,
    },
    {
      field: "is_private",
      value: true,
      label: "Private record groups",
      isolation: { is_public: true },
    },
  ],
  filters: [
    {
      label: "Parent type",
      selection: "single",
      type: "generic",
      field: "parent_type",
      fetcher: recordTypes,
      isolation: false,
    },
    {
      label: "Owner",
      selection: "single",
      type: "users",
      field: "owner",
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
  {
    label: "Least records",
    value: {
      column: "no_records",
      desc: false,
    },
  },
  {
    label: "Most records",
    value: {
      column: "no_records",
      desc: true,
    },
  },
];
