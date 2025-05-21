export const workflowStagesById = {
  1: "ingestion",
  2: "transcription",
  3: "markup",
  4: "review",
  5: "parsing",
};

export const workflowStagesByName = {
  ingestion: 1,
  transcription: 2,
  markup: 3,
  review: 4,
  parsing: 5,
};

export const workflowTagColours = {
  awaiting: { colour: "deep-purple-1", text: "deep-purple-8" },
  in_progress: { colour: "blue-1", text: "blue-9" },
  assessing: { colour: "orange-1", text: "orange-9" },
  processed: { colour: "green-1", text: "green-10" },
  completed: { colour: "green-1", text: "green-10" },
  pending: { colour: "grey-1", text: "grey-5" },
  unknown: { colour: "red-1", text: "red-10" },
  publication: { colour: "teal-1", text: "teal-9" },
  help: { colour: "red-1", text: "red-10" },
  processing: { colour: "orange-1", text: "orange-9" },
};

export const workflowIconbyStatus = {
  1: "change_circle",
  3: "o_task_alt",
};

export const workflowIconbyStage = {
  1: "o_arrow_circle_up", // ingestion
  2: "o_build_circle", // transcription
  3: "o_playlist_add_circle", // markup
  4: "o_recommend", // review
  5: "o_swap_horizontal_circle", // parsing
};

export const workflowIconbyLabel = {
  ingestion: "o_arrow_circle_up",
  transcription: "o_build_circle",
  markup: "o_playlist_add_circle",
  review: "o_recommend",
  parsing: "o_swap_horizontal_circle",
  publication: "o_public",
  help: "o_flag",
  assessing: "change_circle",
  completed: "o_task_alt",
  processing: "arrow_circle_right",
};
