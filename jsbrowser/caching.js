// BUG: this file is served without cache-control headers, so browsers
// BUG: cache it aggressively; after a bug fix is deployed, users may
// BUG: continue to receive and run this stale version until the cache expires

var APP_VERSION = "1.0.0";

function formatPrice(cents) {
  return "$" + (cents / 100).toFixed(2); // BUG in logic: should divide by 100
}
