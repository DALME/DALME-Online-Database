export const filterList = {
  preset: [
    {
      field: "is_active",
      value: true,
      label: "Active users",
      isolation: false,
    },
    {
      field: "is_active",
      value: false,
      label: "Inactive users",
      isolation: false,
    },
    {
      field: "is_staff",
      value: true,
      label: "Staff members",
      isolation: false,
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
