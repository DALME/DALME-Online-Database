/* Cloudfront function viewer-request event handler.

  This is overly aggressive for debugging purposes.

*/

async function handler(event) {
  var request = event.request;
  var uri = request.uri;

  if (!uri.includes('favicon')) {
    request.uri = '/index.html'
  }

  return request;
}
