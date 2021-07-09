const archives = {
  id: "ID",
  name: "Name",
  noRecords: "No. Records",
  locale: "Locale",
  defaultRights: "Default Rights",
  url: "Web Address",
};

const archivalFiles = {
  id: "ID",
  name: "Name",
  primaryDataset: "Primary Dataset",
  owner: "Owner",
  isPrivate: "Private",
  noRecords: "No. Records",
  locale: "Locale(s)",
  authority: "Authority",
  format: "Format",
  support: "Support",
};

const records = {
  id: "ID",
  name: "Name",
  noFolios: "No. Folios",
  owner: "Owner",
  isPrivate: "Private",
  locale: "Locale(s)",
  recordType: "Record Type",
  date: "Date",
  language: "Languages",
  status: "Status",
  helpFlag: "Help",
  activity: "Activity",
  isPublic: "Public",
};

const bibliographies = {
  id: "ID",
  name: "Name",
  primaryDataset: "Primary Dataset",
  defaultRights: "Default Rights",
  zoteroKey: "Zotero Key",
  owner: "Owner",
  isPrivate: "Is Private",
  noRecords: "No. Records",
};

export const columnsByKind = (kind) => {
  return {
    archives,
    archivalFiles,
    records,
    bibliographies,
  }[kind];
};
