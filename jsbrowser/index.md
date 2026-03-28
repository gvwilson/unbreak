# JavaScript Fundamentals and the Browser

## var Hoisting in Loops

A JavaScript function that collects form field values returns `undefined` for some
fields; the bug is using `var` inside a loop, whose hoisting causes the variable
to be shared across iterations. Teaches `var` hoisting, block scope, and why
`let` and `const` are preferable.

## Dead DOM Event Listener

A button click handler works once but stops working after the page is partially
updated; the bug is attaching the event listener to a DOM element that is replaced
by the update, so the listener is discarded. Teaches event delegation and the
difference between live and dead DOM references.

## this Binding in Callbacks

A function that updates a counter when a button is clicked increments by the wrong
amount; the bug is that `this` inside the callback refers to the button element,
not the object that owns the counter. Teaches `this` binding in JavaScript callbacks
and how to use arrow functions or `.bind()` to preserve context.

## Promise Not Awaited

A page that fetches data from an API on load displays stale data; the bug is that
the fetch result is used before the Promise resolves (i.e., code runs synchronously
after an async call). Teaches the JavaScript event loop, Promises, and `async/await`.

## localStorage in Private Mode

A script that reads values from `localStorage` fails silently in private browsing
mode; the bug is that `localStorage` throws a `SecurityError` in that context but
the code has no try/catch. Teaches browser storage limitations and how to use the
browser console and DevTools to observe thrown exceptions.

## Missing Viewport Meta Tag

A page layout breaks on narrow screens even though the CSS looks correct; the bug
is a missing `<meta name="viewport">` tag that prevents mobile scaling. Teaches
how to use browser DevTools' device emulation and inspect computed styles.

## CORS Header Missing

A fetch request to a local API returns a CORS error in the browser but works from
the command line; the bug is a missing `Access-Control-Allow-Origin` header on
the server response. Teaches what CORS is, how to read network error messages in
DevTools, and how to configure server headers.

## Browser Caching Stale JavaScript

A page shows outdated content after a bug fix is deployed; the bug is that the
browser is serving a cached version of the JavaScript file. Teaches cache-control
headers, hard refresh vs. normal refresh, and how to use DevTools to disable the
cache during development.

## Missing Source Map

A JavaScript error is reported on a minified line number that does not correspond
to the source; the bug is deploying a minified bundle without a source map.
Teaches what source maps are, how to generate them, and how to load them in
DevTools to see original source locations.

## Content Security Policy Block

A web application works correctly in development but shows blank content in
production; the bug is a Content Security Policy header that blocks an inline
script. Teaches how to read CSP violation reports in the browser console, how CSP
directives work, and how to move inline scripts to external files to comply.
