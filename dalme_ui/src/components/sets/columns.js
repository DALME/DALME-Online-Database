const collections = {
  id: "ID",
  name: "Name",
  memberCount: "Members",
  description: "Description",
  isPublic: "Public",
  hasLanding: "Landing",
  owner: "Owner",
  permissions: "Permissions",
};

const corpora = {
  id: "ID",
  name: "Name",
  memberCount: "Members",
  description: "Description",
  owner: "Owner",
  permissions: "Permissions",
};

const datasets = {
  id: "ID",
  name: "Name",
  memberCount: "Members",
  description: "Description",
  owner: "Owner",
  datasetUsergroup: "DS Group",
};

const worksets = {
  id: "ID",
  name: "Name",
  memberCount: "Members",
  description: "Description",
  owner: "Owner",
  endpoint: "Endpoint",
  permissions: "Permissions",
};

export const columnsByType = (type) => {
  return {
    collections,
    corpora,
    datasets,
    worksets,
  }[type];
};
