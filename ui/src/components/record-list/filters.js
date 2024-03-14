export const filterList = (userId) => ({
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
      value: userId,
      label: "Your issues",
    },
    {
      field: "assigned_to",
      value: userId,
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
});

export const sortList = () => [
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
];
