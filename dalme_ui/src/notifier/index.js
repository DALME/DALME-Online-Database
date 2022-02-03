import auth from "./auth";
import comments from "./comments";
import CRUD from "./crud";
import tasks from "./tasks";
import tickets from "./tickets";

const notifier = {
  auth,
  comments,
  CRUD,
  tasks,
  tickets,
};

export default notifier;
