import { requests } from "@/api";
import { filterItemClass, filterItemClassSelected, optionFetcher, userFetcher } from "@/components";
import { OptionListSchema } from "@/schemas";

const recordTypes = () =>
  optionFetcher(
    requests.attributeTypes.getAttributeTypeOptions("record_type", true),
    OptionListSchema,
  );

const wfStatusList = [
  {
    label: "Assessing",
    value: "wf_status=1",
    class: filterItemClass,
    classSelected: filterItemClassSelected,
  },
  {
    label: "Awaiting",
    isGroup: true,
    class: filterItemClass,
    classSelected: filterItemClassSelected,
    options: [
      {
        label: "Ingestion",
        value: "wf_status=2,stage=1",
        group: "Awaiting",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Transcription",
        value: "wf_status=2,stage=2",
        group: "Awaiting",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Markup",
        value: "wf_status=2,stage=3",
        group: "Awaiting",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Review",
        value: "wf_status=2,stage=4",
        group: "Awaiting",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Parsing",
        value: "wf_status=2,stage=5",
        group: "Awaiting",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
    ],
  },
  {
    label: "In progress",
    isGroup: true,
    class: filterItemClass,
    classSelected: filterItemClassSelected,
    options: [
      {
        label: "Ingestion",
        value: "wf_status=2,stage=1,done",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Transcription",
        value: "wf_status=2,stage=2,done",
        group: "In progress",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Markup",
        value: "wf_status=2,stage=3,done",
        group: "In progress",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Review",
        value: "wf_status=2,stage=4,done",
        group: "In progress",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
      {
        label: "Parsing",
        value: "wf_status=2,stage=5,done",
        group: "In progress",
        class: filterItemClass,
        classSelected: filterItemClassSelected,
      },
    ],
  },
  {
    label: "Processed",
    value: "wf_status=3",
    class: filterItemClass,
    classSelected: filterItemClassSelected,
  },
];

/*
locale
language
record date
source type
*/

export const filterList = (userId) => ({
  preset: [
    {
      field: "owner",
      value: userId,
      label: "Your records",
      isolation: false,
    },
    {
      field: "is_private",
      value: true,
      label: "Private records",
      isolation: { is_public: true },
    },
    {
      field: "is_public",
      value: true,
      label: "Public records",
      isolation: { is_private: true },
    },
    {
      field: "help_flag",
      value: true,
      label: "Records where help is needed",
      isolation: false,
    },
  ],
  filters: [
    {
      label: "Type",
      selection: "single",
      type: "generic",
      field: "record_type",
      fetcher: recordTypes,
      group: true,
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
    {
      label: "Status",
      selection: "single",
      type: "generic",
      field: "status",
      items: wfStatusList,
      isolation: false,
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
    label: "Least folios",
    value: {
      column: "no_folios",
      desc: false,
    },
  },
  {
    label: "Most folios",
    value: {
      column: "no_folios",
      desc: true,
    },
  },
];
