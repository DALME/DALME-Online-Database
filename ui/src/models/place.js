import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";

import { requests } from "@/api";
import { CustomModel, CustomRepository, Locations, Users } from "@/models";
import { placeListSchema, placeSchema } from "@/schemas";

class Place extends CustomModel {
  static entity = "place";
  static requests = requests.places;
  static schema = {
    instance: placeSchema,
    list: placeListSchema,
  };

  static autoFields = {
    creationUserId: Users,
    modificationUserId: Users,
    locationId: Locations,
  };

  static fields() {
    return {
      attestationCount: this.number(0),
      attributes: this.attr([]),
      commentCount: this.number(0),
      creationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      id: this.attr(null),
      locationId: this.attr(null),
      modificationTimestamp: this.attr(null),
      modificationUserId: this.attr(null),
      name: this.string(""),
      recordAttestationCount: this.number(0),
      tags: this.attr([]),
      // related
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      location: this.belongsTo(Locations, "locationId"),
    };
  }

  static casts() {
    return {
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }
}

class PlaceRepo extends CustomRepository {
  use = Place;
}

export const Places = useRepo(PlaceRepo);
