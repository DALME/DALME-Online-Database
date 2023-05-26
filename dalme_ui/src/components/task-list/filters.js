import { useAuthStore } from "@/stores/auth";
const $authStore = useAuthStore();

export const filterList = {
  preset: [
    {
      field: "completed",
      value: 1,
      label: "Completed tasks",
    },
    {
      field: "completed",
      value: 0,
      label: "Uncompleted tasks",
    },
    {
      field: "creation_user",
      value: $authStore.userId,
      label: "Tasks you created",
    },
    {
      field: "assigned_to",
      value: $authStore.userId,
      label: "Tasks assigned to you",
    },
  ],
};

export const sortList = [
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
