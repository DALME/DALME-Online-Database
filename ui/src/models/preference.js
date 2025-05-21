import { useRepo } from "pinia-orm";
import { ref } from "vue";

import { requests } from "@/api";
import { CustomModel, CustomRepository } from "@/models";
import { preferenceListSchema, preferenceSchema } from "@/schemas";

class Preference extends CustomModel {
  static entity = "preference";
  static primaryKey = "name";
  static requests = requests.preferences;
  static schema = {
    instance: preferenceSchema,
    list: preferenceListSchema,
  };

  static piniaOptions = {
    ready: ref(false),
  };

  static fields() {
    return {
      name: this.string(""),
      label: this.string(""),
      description: this.string(""),
      dataType: this.string(""),
      group: this.string(""),
      default: this.attr(null),
      value: this.attr(null),
    };
  }
}

class PreferenceRepo extends CustomRepository {
  use = Preference;

  // getters
  get isReady() {
    return this.store.ready;
  }

  // actions
  init() {
    if (this.store.ready) return Promise.resolve();
    return new Promise((resolve) => {
      this.remoteRetrieve().then(() => {
        this.store.ready = true;
        resolve();
      });
    });
  }

  get(name) {
    const rec = this.query().find(name);
    return rec ? rec.value : null;
  }

  set(name, value) {
    return this.update(name, { value });
  }
}

export const Preferences = useRepo(PreferenceRepo);
