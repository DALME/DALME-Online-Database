import auth from "./auth";
import comments from "./comments";
import CRUD from "./crud";
import tasks from "./tasks";

const notifier = {
  auth,
  comments,
  CRUD,
  tasks,
};

export default notifier;
