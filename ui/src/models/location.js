import { useRepo } from "pinia-orm";

import { requests } from "@/api";
import { Attributes, CustomModel, CustomRepository } from "@/models";
import { locationListSchema, locationSchema } from "@/schemas";

class Location extends CustomModel {
  static entity = "location";
  static requests = requests.locations;
  static schema = {
    instance: locationSchema,
    list: locationListSchema,
  };

  static autoFields = {
    attributeIds: Attributes,
  };

  static fields() {
    return {
      attributeIds: this.attr([]),
      id: this.attr(null),
      locationType: this.string(""),
      // related
      attributes: this.hasManyBy(Attributes, "attributeIds"),
    };
  }
}

class LocationRepo extends CustomRepository {
  use = Location;
}

export const Locations = useRepo(LocationRepo);
