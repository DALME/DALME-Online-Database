// "agents": [
//     {
//         "id": "17a935c3-6203-4674-937d-8ab56826132a",
//         "name": "<unclear>Connuccio</unclear> condam Guidi bicchierario contrate burgi Sancti Fridiani",
//         "type": "Person",
//         "legal_persona": "creditor"
//     },
// ]

export const empty = () => ({
  agent: null,
  legalPersona: null,
  type: "person",
});

export const normalizeAgentsInput = (input) => input;
export const normalizeAgentsOutput = (output) => output;

// Make sure to purge any values that are just the 'empty' field itself and to
// null out the payload if there's no data at all.
// export const normalizeOutputSchema = yup
//   .array()
//   .nullable()
//   .compact((value) => value === empty())
//   .of(agentFieldOutputSchema)
//   .transform((final) => (isEmpty(final) ? null : final));
