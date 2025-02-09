export const filterList = (userId) => ({
  preset: [
    {
      field: "completed",
      value: true,
      label: "Completed tasks",
      isolation: false,
    },
    {
      field: "completed",
      value: false,
      label: "Uncompleted tasks",
      isolation: false,
    },
    {
      field: "creation_user",
      value: userId,
      label: "Tasks you created",
      isolation: false,
    },
    {
      field: "assigned_to",
      value: userId,
      label: "Tasks assigned to you",
      isolation: false,
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
