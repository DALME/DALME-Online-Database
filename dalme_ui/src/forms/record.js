import { markRaw } from "vue";

import { fetcher, requests } from "@/api";
import {
  AttributesField,
  InputField,
  SelectField,
  TextField,
} from "@/components/forms";
import {
  recordCreateValidator,
  recordUpdateValidator,
  recordPostSchema,
  recordPutSchema,
  userListSchema,
} from "@/schemas";

const recordFormSchema = [
  // Step 1
  [
    // type
    {
      model: "name",
      component: markRaw(InputField),
      label: "Name",
    },
    {
      model: "shortName",
      component: markRaw(InputField),
      label: "Short name",
    },
    // list
    {
      model: "description",
      component: markRaw(TextField),
      label: "Description",
    },
    {
      model: "owner",
      component: markRaw(SelectField),
      label: "Owner",
      filterable: true,
      getOptions: () =>
        fetcher(requests.users.getUsers()).then((response) => response.json()),
      optionLabel: "fullName",
      optionsSchema: userListSchema,
    },
    // parent
    // primaryDataset
  ],
  // Step 2 - Attributes
  [
    {
      model: "attribute",
      component: markRaw(AttributesField),
    },
  ],
];

const recordRequests = {
  create: (data) => requests.sources.createSource(data),
  update: ({ id, ...data }) => requests.sources.editSource(id, data),
};

const recordFormValidators = {
  create: recordCreateValidator,
  update: recordUpdateValidator,
};

const submitSchemas = {
  create: recordPostSchema,
  update: recordPutSchema,
};

export default {
  requests: recordRequests,
  schema: recordFormSchema,
  validators: recordFormValidators,
  submitSchemas,
};
