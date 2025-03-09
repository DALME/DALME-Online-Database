const processData = (data) => {
  return {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Records types",
        barPercentage: 0.5,
        barThickness: 6,
        maxBarThickness: 8,
        minBarLength: 2,
        data: Object.values(data),
      },
    ],
  };
};

export const RecordTypes = {
  id: "record-types",
  type: "bar",
  title: "Records by type",
  options: { responsive: true },
  query: {
    target: "Record",
    cat1: "record_type",
  },
  handler: processData,
};
