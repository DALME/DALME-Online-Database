import { isNil, map } from "ramda";
import { fetcher } from "@/boot/axios";
import { requests } from "@/api";
import { attachmentSchema } from "@/schemas";

export const resolveAttachments = async (records, targetField = "file") => {
  const resolveAttachment = async (record) => {
    if (!isNil(record[targetField])) {
      const response = await fetcher(
        requests.attachments.getAttachment(record[targetField]),
      );
      if (response.status === 200) {
        await attachmentSchema
          .validate(response.data, { stripUnknown: true })
          .then((value) => (record[targetField] = value));
      }
    }
    return record;
  };
  return Promise.all(map(resolveAttachment, records));
};
