import attributes from "./attributes";
import auth from "./auth";
import clipboard from "./clipboard";
import comments from "./comments";
import CRUD from "./crud";
import editor from "./editor";
import records from "./records";
import settings from "./settings";
import tasks from "./tasks";
import tickets from "./tickets";
import transcriptions from "./transcriptions";
import users from "./users";
import workflow from "./workflow";

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
