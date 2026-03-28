// Original readable source — not loaded by the page.
// This would be compiled/minified into sourcemap.min.js for deployment.
// Without a source map, errors point into the minified file, not here.

function processItems(items) {
  return items.map(function (item) {
    return item.toUpperCase(); // TypeError at runtime: numbers have no toUpperCase
  });
}

document.getElementById("run-btn").addEventListener("click", function () {
  var items = [1, 2, 3]; // BUG: numbers passed where strings are expected
  var result = processItems(items);
  document.getElementById("output").textContent = result.join(", ");
});
