const archives = {
  name: "Name",
  noRecords: "No. Records",
  locale: "Locale",
  defaultRights: "Default Rights",
  archiveUrl: "Web Address",
};

const archivalFiles = {
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

const bibliography = {
  name: "Name",
  primaryDataset: "Primary Dataset",
  defaultRights: "Default Rights",
  zoteroKey: "Zotero Key",
  owner: "Owner",
  isPrivate: "Is Private",
  noRecords: "No. Records",
};

export const columnsByType = (sourceType) => {
  return {
    archives,
    archivalFiles,
    records,
    bibliography,
  }[sourceType];
};
