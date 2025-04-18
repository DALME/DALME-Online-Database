import { default as ticketRequests } from "@/api/tickets.js";
import { default as userRequests } from "@/api/users.js";
import { fetcher } from "@/boot/axios";
import { ticketListSchema } from "@/schemas/tickets.js";
import { userListSchema } from "@/schemas/users.js";
import { nully } from "@/utils/utilities.js";

export const filterItemClass = "text-grey-8";
export const filterItemClassSelected = "text-weight-bold bg-indigo-1 text-indigo-5";

export const optionFetcher = (request, validationSchema, cls, clsSel, icn) => {
  return new Promise((resolve) => {
    fetcher(request).then((response) => {
      if (response.status === 200) {
        validationSchema.validate(response.data, { stripUnknown: false }).then((value) => {
          let result = value.map((x) => ({
            label: x.label,
            value: x.value,
            group: x.group,
            class: cls || filterItemClass,
            classSelected: clsSel || filterItemClassSelected,
            icon: icn || null,
          }));
          resolve(result);
        });
      }
    });
  });
};

export const ticketFetcher = (filter) => {
  return new Promise((resolve) => {
    const query = nully(filter)
      ? "ordering=id&limit=10&offset=0"
      : `ordering=id&search=${filter}&limit=10&offset=0`;
    fetcher(ticketRequests.getTickets(query)).then((response) => {
      if (response.status === 200) {
        ticketListSchema.validate(response.data.data, { stripUnknown: true }).then((value) => {
          resolve(value);
        });
      }
    });
  });
};

export const userFetcher = (filter) => {
  return new Promise((resolve) => {
    const query = nully(filter)
      ? "ordering=id&limit=10&offset=0"
      : `ordering=id&search=${filter}&limit=10&offset=0`;
    fetcher(userRequests.getUsers(query)).then((response) => {
      if (response.status === 200) {
        userListSchema.validate(response.data.data, { stripUnknown: true }).then((value) => {
          resolve(value);
        });
      }
    });
  });
};
