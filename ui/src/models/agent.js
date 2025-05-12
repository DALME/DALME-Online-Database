import { useRepo } from "pinia-orm";

import { requests } from "@/api";
import { CustomModel, CustomRepository, Users } from "@/models";
import { agentListSchema, agentSchema } from "@/schemas";

class Agent extends CustomModel {
  static entity = "agent";
  static requests = requests.agents;
  static schema = {
    instance: agentSchema,
    list: agentListSchema,
  };

  static autoFields = {
    userId: Users,
  };

  static fields() {
    return {
      agentType: this.string(""),
      attestationCount: this.number(0),
      id: this.attr(null),
      name: this.string(""),
      recordAttestationCount: this.number(0),
      userId: this.attr(null),
      // related
      user: this.belongsTo(Users, "userId"),
    };
  }
}

class AgentRepo extends CustomRepository {
  use = Agent;
}

export const Agents = useRepo(AgentRepo);
