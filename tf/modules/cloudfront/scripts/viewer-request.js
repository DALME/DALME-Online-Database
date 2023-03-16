/* Cloudfront function viewer-request event handler. */

function handler(event) {
  var request = event.request;
  var uri = request.uri;

  if (!uri.includes('.') && !uri.endsWith('/')) {
    request.uri += '/';
  }

  request.uri = request.uri.replace(/^\/[^/]*\//, '/');

  if (!uri.includes('.')) {
    request.uri += 'index.html';
  }

  return request;
}
