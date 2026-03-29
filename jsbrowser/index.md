# JavaScript Fundamentals and the Browser

## `var` Hoisting in Loops {: #jsbrowser-hoisting}

Open the page in a browser, fill in some form field values, and submit. Check the
console output. Are all the field values captured and reported correctly?

[% inc hoisting.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A JavaScript function that collects form field values returns `undefined` for some
fields; the bug is using `var` inside a loop, whose hoisting causes the variable
to be shared across iterations. Teaches `var` hoisting, block scope, and why
`let` and `const` are preferable.

</details>

## Dead DOM Event Listener {: #jsbrowser-deaddom}

Open the page and click the button several times. Does it keep working after the
first click?

[% inc deaddom.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A button click handler works once but stops working after the page is partially
updated; the bug is attaching the event listener to a DOM element that is replaced
by the update, so the listener is discarded. Teaches event delegation and the
difference between live and dead DOM references.

</details>

## `this` Binding in Callbacks {: #jsbrowser-thisbind}

Open the page and click the button several times. Does the counter increment by the
expected amount each time?

[% inc thisbind.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A function that updates a counter when a button is clicked increments by the wrong
amount; the bug is that `this` inside the callback refers to the button element,
not the object that owns the counter. Teaches `this` binding in JavaScript callbacks
and how to use arrow functions or `.bind()` to preserve context.

</details>

## Promise Not Awaited {: #jsbrowser-unawaited}

Open the page and check the data displayed against what the API returns. Is the
data correct on the first load, or does it appear stale or blank?

[% inc unawaited.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A page that fetches data from an API on load displays stale data; the bug is that
the fetch result is used before the Promise resolves (i.e., code runs synchronously
after an async call). Teaches the JavaScript event loop, Promises, and `async/await`.

</details>

## `localStorage` in Private Mode {: #jsbrowser-localstorage}

Open the page in a private browsing window. Does anything go wrong? Check the
browser console for errors.

[% inc localstorage.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A script that reads values from `localStorage` fails silently in private browsing
mode; the bug is that `localStorage` throws a `SecurityError` in that context but
the code has no try/catch. Teaches browser storage limitations and how to use the
browser console and DevTools to observe thrown exceptions.

</details>

## Missing Viewport `meta` Tag {: #jsbrowser-viewport}

Open the page in a browser and use DevTools to simulate a narrow mobile screen.
Does the layout look correct?

[% inc viewport.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A page layout breaks on narrow screens even though the CSS looks correct; the bug
is a missing `<meta name="viewport">` tag that prevents mobile scaling. Teaches
how to use browser DevTools' device emulation and inspect computed styles.

</details>

## CORS Header Missing {: #jsbrowser-cors}

Open the HTML page in a browser and check the network tab in DevTools. Does the
fetch request succeed, or do you see an error? Compare this with running the same
request from the command line.

[% inc cors_server.py scrub="\s*# BUG.*" %]
[% inc cors.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A fetch request to a local API returns a CORS error in the browser but works from
the command line; the bug is a missing `Access-Control-Allow-Origin` header on
the server response. Teaches what CORS is, how to read network error messages in
DevTools, and how to configure server headers.

</details>

## Browser Caching Stale JavaScript {: #jsbrowser-caching}

Make a change to the JavaScript file and reload the page normally. Does the change
take effect? Try checking the network tab in DevTools to see which version of the
file the browser is serving.

[% inc caching.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc caching.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A page shows outdated content after a bug fix is deployed; the bug is that the
browser is serving a cached version of the JavaScript file. Teaches cache-control
headers, hard refresh vs. normal refresh, and how to use DevTools to disable the
cache during development.

</details>

## Missing Source Map {: #jsbrowser-sourcemap}

Trigger the JavaScript error and look at the stack trace in the browser console.
Can you identify the exact source location of the problem from the information
shown?

[% inc sourcemap_original.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc sourcemap.min.js scrub="\s*(//|<!--).*BUG.*" %]
[% inc sourcemap.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A JavaScript error is reported on a minified line number that does not correspond
to the source; the bug is deploying a minified bundle without a source map.
Teaches what source maps are, how to generate them, and how to load them in
DevTools to see original source locations.

</details>

## Content Security Policy Block {: #jsbrowser-csp}

Open the page in a browser. Does the inline script run? Check the console for any
policy-related messages.

[% inc csp.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A web application works correctly in development but shows blank content in
production; the bug is a Content Security Policy header that blocks an inline
script. Teaches how to read CSP violation reports in the browser console, how CSP
directives work, and how to move inline scripts to external files to comply.

</details>
