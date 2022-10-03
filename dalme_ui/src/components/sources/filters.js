import { useAuthStore } from "@/stores/auth";
const $authStore = useAuthStore();

const filters = {
  records: {
    preset: [
      {
        field: "status",
        value: 0,
        label: "Open issues",
      },
      {
        field: "status",
        value: 1,
        label: "Closed issues",
      },
      {
        field: "creation_user",
        value: $authStore.userId,
        label: "Your issues",
      },
      {
        field: "assigned_to",
        value: $authStore.userId,
        label: "Assigned to me",
      },
    ],
    filters: [
      {
        dropDownLabel: "Tags",
        type: "multiple",
        menuItems: [
          {
            field: "status",
            value: 0,
            label: "Open issues",
          },
        ],
      },
      {
        dropDownLabel: "Author",
        type: "single",
        menuItems: [
          {
            field: "status",
            value: 0,
            label: "Open issues",
          },
        ],
      },
      {
        dropDownLabel: "Assignee",
        type: "single",
        menuItems: [
          {
            field: "status",
            value: 0,
            label: "Open issues",
          },
        ],
      },
    ],
  },
};

const sortLists = {
  records: [
    {
      label: "Newest",
      value: "-creation_timestamp",
    },
    {
      label: "Oldest",
      value: "creation_timestamp",
    },
    {
      label: "Most commented",
      value: "-no_comments",
    },
    {
      label: "Least commented",
      value: "no_comments",
    },
    {
      label: "Recently updated",
      value: "-modification_timestamp",
    },
    {
      label: "Least recently updated",
      value: "modification_timestamp",
    },
  ],
};

export const filtersByType = (sourceType) => {
  return filters[sourceType];
};

export const sortByType = (sourceType) => {
  return sortLists[sourceType];
};
