import { Query } from "pinia-orm";

export default class CustomQuery extends Query {
  normalize(records) {
    let processedData = this.newInterpreter().process(records);
    const modelTypes = this.model.$types();
    const isChildEntity =
      this.model.$baseEntity() !== this.model.$entity() ||
      this.model.$baseNamespace() !== this.model.$namespace();

    if (Object.values(modelTypes).length > 0 || isChildEntity) {
      const modelTypesKeys = Object.keys(modelTypes);
      const recordsByTypes = {};
      records = Array.isArray(records) ? records : [records];

      records.forEach((record) => {
        const recordType =
          modelTypesKeys.includes(`${record[this.model.$typeKey()]}`) || isChildEntity
            ? (record[this.model.$typeKey()] ??
              this.model.$fields()[this.model.$typeKey()].defaultValue)
            : modelTypesKeys[0];
        if (!recordsByTypes[recordType]) {
          recordsByTypes[recordType] = [];
        }
        recordsByTypes[recordType].push(record);
      });

      for (const entry in recordsByTypes) {
        const typeModel = modelTypes[entry];
        if (typeModel.modelEntity() === this.model.$modelEntity()) {
          processedData = this.newInterpreter().process(recordsByTypes[entry]);
        } else {
          this.newQueryWithConstraints(typeModel.modelEntity()).save(recordsByTypes[entry]);
        }
      }
    }

    return processedData;
  }

  saveEntities(entities) {
    for (const entity in entities) {
      const query = this.newQuery(entity);
      const elements = entities[entity];
      query.saveElements(elements);
    }
  }
}
