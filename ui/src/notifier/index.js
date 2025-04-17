import auth from "./auth";
import comments from "./comments";
import clipboard from "./clipboard";
import CRUD from "./crud";
import tasks from "./tasks";
import tickets from "./tickets";
import users from "./users";
import transcriptions from "./transcriptions";
import settings from "./settings";
import workflow from "./workflow";
import records from "./records";
import attributes from "./attributes";
import editor from "./editor";

const notifier = {
  attributes,
  auth,
  comments,
  clipboard,
  CRUD,
  records,
  settings,
  tasks,
  tickets,
  transcriptions,
  users,
  workflow,
  editor,
};

export default notifier;
