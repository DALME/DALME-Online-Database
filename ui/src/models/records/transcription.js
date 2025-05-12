import { useRepo } from "pinia-orm";

import { CustomModel, CustomRepository } from "@/models";

class Transcription extends CustomModel {
  static entity = "transcription";

  static fields() {
    return {
      author: this.string(""),
      id: this.attr(null),
      pageId: this.attr(null),
      transcription: this.string(""),
      version: this.number(0),
    };
  }
}

class TranscriptionRepo extends CustomRepository {
  use = Transcription;
}

export const Transcriptions = useRepo(TranscriptionRepo);
