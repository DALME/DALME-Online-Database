/* eslint-disable no-console */
const isDev = process.env.NODE_ENV === "development";

const logger = {
  log: (message, ...args) => {
    if (isDev) console.log(message, args);
  },
  error: (err) => {
    if (isDev) console.error(err);
  },
};

export default logger;
