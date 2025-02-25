/* Cloudfront function viewer-request event handler. */

async function handler(event) {
  var request = event.request;
  var uri = request.uri;

  // If we aren't requesting some file (with a .extension) then we need to
  // resolve the root object and remove any subdfolders. They will still appear
  // in the URL and will be handled by vue-router.
  if (!uri.includes('.')) {
    request.uri = '/index.html';
  } else {
    // Removes the first segment of the URL path, ie. 'db/'.
    request.uri = request.uri.replace(/^\/[^/]*\//, '/');
  }

  return request;
}
