import { markRaw } from "vue";
import { InputField, TextField } from "@/components/forms";
import { taskValidator } from "@/schemas";

const formSchema = {
  title: {
    component: markRaw(InputField),
    label: "Task title",
  },
  description: {
    component: markRaw(TextField),
    label: "Task description",
  },
};

export default {
  schema: formSchema,
  validator: taskValidator,
};
