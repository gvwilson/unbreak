# JavaScript Fundamentals and the Browser

## Attach click handlers to a list of buttons {: #jsbrowser-hoisting}

Open the page in a browser, fill in some form field values, and submit. Check the
console output. Are all the field values captured and reported correctly?

[% inc hoisting.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `var` inside a loop. Hoisting causes the variable to be shared
across iterations, so the function returns `undefined` for some fields.

Shows: `var` hoisting, block scope, and why `let` and `const` are
preferable.

To find it: open the browser console after submitting the form. Look at which fields
report `undefined`. Then read the `var` declaration: because `var` is
function-scoped and hoisted, all loop iterations share the same variable, and by the
time a callback runs that variable holds its final loop value rather than the value
from the iteration that created the callback.

</details>

## Update a table row when a button is clicked {: #jsbrowser-deaddom}

Open the page and click the button several times. Does it keep working after the
first click?

[% inc deaddom.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is attaching the event listener to a DOM element that is replaced by the
update, so the listener is discarded and the button stops working after the first
click.

Shows: event delegation and the difference between live and dead DOM
references.

To find it: click the button a second time and check the console for errors. If no
error appears but nothing happens, open DevTools and inspect the DOM — the original
button element has been replaced and no longer exists, so the event listener
attached to it is gone.

</details>

## Save a form field value with a timer {: #jsbrowser-thisbind}

Open the page and click the button several times. Does the counter increment by the
expected amount each time?

[% inc thisbind.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `this` inside the callback refers to the button element rather than
the object that owns the counter, so the counter increments by the wrong amount.

Shows: `this` binding in JavaScript callbacks and how to use arrow
functions or `.bind()` to preserve context.

To find it: add `console.log(this)` as the first line of the callback. If it logs a
button element instead of the owning object, `this` is bound to the event target.
Use an arrow function or `.bind(this)` to preserve the correct context.

</details>

## Fetch user data before rendering a profile {: #jsbrowser-unawaited}

Open the page and check the data displayed against what the API returns. Is the
data correct on the first load, or does it appear stale or blank?

[% inc unawaited.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the fetch result is used before the Promise resolves (code runs
synchronously after an async call), so the page displays stale data.

Shows: the JavaScript event loop, Promises, and `async/await`.

To find it: open the Network tab in DevTools and watch when the fetch request
completes relative to when data is rendered. If the render happens before the
network request finishes, the code is not waiting for the promise to resolve. Add
`console.log(data)` immediately before and after the `await` to see when data
becomes available.

</details>

## Save user preferences across page loads {: #jsbrowser-localstorage}

Open the page in a private browsing window. Does anything go wrong? Check the
browser console for errors.

[% inc localstorage.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `localStorage` throws a `SecurityError` in private browsing mode but
the code has no try/catch, so the script fails silently.

Shows: browser storage limitations and how to use the browser console
and DevTools to observe thrown exceptions.

To find it: open the browser Console tab after loading the page in private mode. A
`SecurityError` will appear there even though the page looks normal. Wrapping the
`localStorage` access in a `try/catch` and printing the error message confirms the
exact line that throws.

</details>

## Build a page that works on mobile devices {: #jsbrowser-viewport}

Open the page in a browser and use DevTools to simulate a narrow mobile screen.
Does the layout look correct?

[% inc viewport.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `<meta name="viewport">` tag that prevents mobile scaling, so
the page layout breaks on narrow screens even though the CSS looks correct.

Shows: how to use browser DevTools' device emulation and inspect
computed styles.

To find it: open DevTools, click the device-emulation icon (phone/tablet), select a
narrow screen width, and reload. If the layout overflows or text appears tiny, check
the page source for a `<meta name="viewport" content="width=device-width,
initial-scale=1">` tag.

</details>

## Load data from an API on a different domain {: #jsbrowser-cors}

Open the HTML page in a browser and check the network tab in DevTools. Does the
fetch request succeed, or do you see an error? Compare this with running the same
request from the command line.

[% inc cors_server.py scrub="\s*# BUG.*" %]
[% inc cors.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `Access-Control-Allow-Origin` header on the server response, so
the fetch request returns a CORS error in the browser even though it works from the
command line.

Shows: what CORS is, how to read network error messages in DevTools,
and how to configure server headers.

To find it: open the Network tab in DevTools, find the failed request, and read the
Console message — it will say the request was blocked by CORS policy. Then run the
same request with `curl` from the terminal — it succeeds, confirming the restriction
is browser-enforced and that the server needs to add the `Access-Control-Allow-Origin`
header.

</details>

## Deploy an update that users don't see {: #jsbrowser-caching}

Make a change to the JavaScript file and reload the page normally. Does the change
take effect? Try checking the network tab in DevTools to see which version of the
file the browser is serving.

[% inc caching.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc caching.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the browser is serving a cached version of the JavaScript file, so
the page shows outdated content after a bug fix is deployed.

Shows: cache-control headers, hard refresh vs. normal refresh, and how
to use DevTools to disable the cache during development.

To find it: open the Network tab in DevTools, reload the page, and look at the
`.js` file entry in the request list. A status of `304` or the label `(from disk
cache)` means the browser did not fetch the updated file. Do a hard reload
(Ctrl+Shift+R on Linux/Windows, Cmd+Shift+R on Mac) to bypass the cache and confirm
the new version loads.

</details>

## Debug a minified production build {: #jsbrowser-sourcemap}

Trigger the JavaScript error and look at the stack trace in the browser console.
Can you identify the exact source location of the problem from the information
shown?

[% inc sourcemap_original.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc sourcemap.min.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc sourcemap.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is deploying a minified bundle without a source map, so JavaScript errors
are reported on minified line numbers that do not correspond to the source.

Shows: what source maps are, how to generate them, and how to load
them in DevTools to see original source locations.

To find it: trigger the error and read the stack trace in the console. If it points
to a single-line file with hundreds of characters separated by semicolons, the
script is minified. Check whether a `.map` file exists alongside the `.min.js` file,
and whether the minified file ends with a `//# sourceMappingURL=` comment.

</details>

## Add an inline script to a secured page {: #jsbrowser-csp}

Open the page in a browser. Does the inline script run? Check the console for any
policy-related messages.

[% inc csp.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a Content Security Policy header that blocks an inline script, so the
application shows blank content in production even though it works in development.

Shows: how to read CSP violation reports in the browser console, how
CSP directives work, and how to move inline scripts to external files
to comply.

To find it: open the Console tab after loading the page. A message starting with
`Content Security Policy` will name the directive that blocked the script (e.g.,
`script-src`). Check the server's `Content-Security-Policy` response header to see
what sources are allowed and which are missing.

</details>
