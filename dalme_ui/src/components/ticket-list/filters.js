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
      label: "Assigned to you",
    },
  ],
});

export const sortList = () => [
  {
    label: "Newest",
    value: {
      column: "creationTimestamp",
      desc: true,
    },
  },
  {
    label: "Oldest",
    value: {
      column: "creationTimestamp",
      desc: false,
    },
  },
  {
    label: "Most commented",
    value: {
      column: "commentCount",
      desc: true,
    },
  },
  {
    label: "Least commented",
    value: {
      column: "commentCount",
      desc: false,
    },
  },
  {
    label: "Recently updated",
    value: {
      column: "modificationTimestamp",
      desc: true,
    },
  },
  {
    label: "Least recently updated",
    value: {
      column: "modificationTimestamp",
      desc: false,
    },
  },
];
