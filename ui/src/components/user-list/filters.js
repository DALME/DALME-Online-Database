export const filterList = {
  preset: [
    {
      field: "is_active",
      value: 1,
      label: "Active users",
    },
    {
      field: "is_active",
      value: 0,
      label: "Inactive users",
    },
    {
      field: "is_staff",
      value: 1,
      label: "Staff members",
    },
  ],
};

export const sortList = [
  {
    label: "Newest",
    value: {
      column: "dateJoined",
      desc: true,
    },
  },
  {
    label: "Name & Surname",
    value: {
      column: "fullName",
      desc: false,
    },
  },
  {
    label: "Last Login",
    value: {
      column: "lastLogin",
      desc: true,
    },
  },
  {
    label: "User Id",
    value: {
      column: "id",
      desc: false,
    },
  },
  {
    label: "Username",
    value: {
      column: "username",
      desc: true,
    },
  },
];
