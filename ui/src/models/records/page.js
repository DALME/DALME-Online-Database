import { useRepo } from "pinia-orm";

import { CustomModel, CustomRepository } from "@/models";

import { Transcriptions } from "./transcription";

class Page extends CustomModel {
  static entity = "page";

  static fields() {
    return {
      damId: this.number(null),
      hasImage: this.boolean(false),
      hasTranscription: this.boolean(false),
      id: this.attr(null),
      manifestUrl: this.string(""),
      name: this.string(""),
      order: this.number(0),
      recordId: this.attr(null),
      thumbnailUrl: this.string(""),
      transcription: this.hasOne(Transcriptions, "pageId"),
    };
  }
}

class PageRepo extends CustomRepository {
  use = Page;
}

export const Pages = useRepo(PageRepo);
