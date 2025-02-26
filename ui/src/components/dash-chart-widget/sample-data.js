export const samples = {
  bar: {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "Bar Dataset",
        barPercentage: 0.5,
        barThickness: 6,
        maxBarThickness: 8,
        minBarLength: 2,
        data: [10, 20, 30, 40, 50, 60, 70],
      },
    ],
  },
  doughnut: {
    labels: ["Red", "Blue", "Yellow"],
    datasets: [
      {
        label: "Doughnut Dataset",
        data: [300, 50, 100],
        backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"],
        hoverOffset: 4,
      },
    ],
  },
  line: {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "Line Dataset",
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  },
  pie: {
    labels: ["A", "B", "C"],
    datasets: [
      {
        label: "Pie Dataset",
        data: [200, 500, 50],
        backgroundColor: ["rgb(99, 255, 132)", "rgb(162, 52, 235)", "rgb(255, 20, 205)"],
        hoverOffset: 4,
      },
    ],
  },
  polar: {
    labels: ["Red", "Green", "Yellow", "Grey", "Blue"],
    datasets: [
      {
        label: "Polar Area Dataset",
        data: [11, 16, 7, 3, 14],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(75, 192, 192)",
          "rgb(255, 205, 86)",
          "rgb(201, 203, 207)",
          "rgb(54, 162, 235)",
        ],
      },
    ],
  },
  radar: {
    labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
    datasets: [
      {
        label: "Radar Dataset 1",
        data: [65, 59, 90, 81, 56, 55, 40],
        fill: true,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgb(255, 99, 132)",
        pointBackgroundColor: "rgb(255, 99, 132)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgb(255, 99, 132)",
      },
      {
        label: "Radar Dataset 2",
        data: [28, 48, 40, 19, 96, 27, 100],
        fill: true,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgb(54, 162, 235)",
        pointBackgroundColor: "rgb(54, 162, 235)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgb(54, 162, 235)",
      },
    ],
  },
  scatter: {
    datasets: [
      {
        label: "Scatter Dataset",
        data: [
          {
            x: -10,
            y: 0,
          },
          {
            x: 0,
            y: 10,
          },
          {
            x: 10,
            y: 5,
          },
          {
            x: 0.5,
            y: 5.5,
          },
        ],
        backgroundColor: "rgb(255, 99, 132)",
      },
    ],
  },
  bubble: {
    datasets: [
      {
        label: "BubbleDataset",
        data: [
          {
            x: 20,
            y: 30,
            r: 15,
          },
          {
            x: 40,
            y: 10,
            r: 10,
          },
        ],
        backgroundColor: "rgb(255, 99, 132)",
      },
    ],
  },
};

export const sampleOptions = {
  bar: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
  radar: {
    responsive: true,
    elements: {
      line: {
        borderWidth: 3,
      },
    },
  },
  scatter: {
    responsive: true,
    scales: {
      x: {
        type: "linear",
        position: "bottom",
      },
    },
  },
};
