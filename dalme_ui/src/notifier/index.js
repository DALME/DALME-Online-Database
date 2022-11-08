import auth from "./auth";
import comments from "./comments";
import CRUD from "./crud";
import tasks from "./tasks";
import tickets from "./tickets";
import users from "./users";
import transcriptions from "./transcriptions";

const notifier = {
  auth,
  comments,
  CRUD,
  tasks,
  tickets,
  users,
  transcriptions,
};

export default notifier;
