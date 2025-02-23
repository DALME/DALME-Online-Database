/* Cloudfront function viewer-request event handler. */

async function handler(event) {
  var request = event.request;
  var uri = request.uri;

  // if (!uri.includes('.') && !uri.endsWith('/')) {
  //   request.uri += '/';
  // }

  // request.uri = request.uri.replace(/^\/[^/]*\//, '/');

  // if (!uri.includes('.')) {
  //   request.uri = '/index.html';
  // }

  // Check whether the URI is missing a file name.
  if (uri.endsWith('/')) {
    request.uri += 'index.html';
  }
  // Check whether the URI is missing a file extension.
  else if (!uri.includes('.')) {
    request.uri += '/index.html';
  }

  return request;
}
