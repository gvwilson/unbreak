# Alpine.js

Alpine.js lets you add reactive behavior to HTML pages by writing `x-data`, `x-bind`,
and `x-on` attributes directly on elements. It evaluates those attributes in a reactive
scope it creates and manages, which means the rules about what is in scope and when
updates happen are subtler than they first appear.
Before trying any of these examples, start the server:

```
uv run server.py
```

Then open `http://localhost:8000` in a browser to see the list of examples,
or navigate directly to `http://localhost:8000/<slug>` for the one you want.

## Toggle a message with a button {: #alpine-wrongscope}

Open the page and click Toggle.
Does the message appear?

[% inc wrongscope.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing `x-data="{ visible: false }"` on an inner `<span>` while
putting `x-show="visible"` and `@click` on the outer `<div>`. Alpine directives
can only read data from `x-data` defined on the same element or one of its
ancestors. A child's `x-data` is invisible to its parent's directives, so
`visible` is undefined in the outer scope and nothing happens.

Shows: Alpine's scope model — `x-data` creates a component boundary; everything
inside it shares that scope, but nothing outside it does.

To find it: open DevTools, click Toggle, and watch the console for an "undefined"
reference. Move `x-data="{ visible: false }"` from the `<span>` to the outer
`<div>` so that `x-show` and `@click` can both see the reactive property.

</details>

## Submit a name and show a confirmation {: #alpine-noprevent}

Type a name and click Submit.
Does the confirmation appear, or does the page reload?

[% inc noprevent.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `@submit` without the `.prevent` modifier. Without `.prevent`,
Alpine runs `submitted = true` and then lets the browser's default form submission
proceed. The browser reloads the page, which destroys the Alpine component and all
its state before the confirmation can ever be shown.

Shows: event modifier syntax in Alpine (`@submit.prevent`) and why `preventDefault()`
is essential whenever a form has a `type="submit"` button.

To find it: watch the address bar after clicking Submit. If it appends `?name=...`
and refreshes, the native action is firing. Change `@submit` to `@submit.prevent`.

</details>

## Show content only after Alpine loads {: #alpine-xcloak}

Reload the page with network throttling enabled in DevTools (Network tab,
set to "Slow 3G"). Is the counter area blank for a moment before the count
appears?

[% inc xcloak.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `x-cloak` is applied to the element, but the CSS rule that hides
it is missing. Alpine removes the `x-cloak` attribute after it initializes the
component, so the intended pattern is: CSS hides the element initially, then Alpine
removes `x-cloak` to reveal it. Without the rule, the element is visible from the
start and shows blank or partially-initialized content before Alpine processes it.

Shows: how `x-cloak` works and why it requires both the attribute *and* the CSS rule:

```css
[x-cloak] { display: none; }
```

To find it: inspect the element and search for `x-cloak` in the Styles panel.
If no rule targets `[x-cloak]`, add one in a `<style>` block in `<head>`, before
the Alpine script tag.

</details>

## Display a greeting from component state {: #alpine-stringdata}

Open the page. Does any text appear in the paragraph?

[% inc stringdata.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `x-data="'hello'"`. Alpine evaluates the attribute value as a JavaScript
expression, which here produces the string `"hello"`. Alpine wraps whatever
`x-data` returns in a reactive proxy, but `"hello".message` is `undefined`, so
`x-text="message"` sets the paragraph to an empty string.

Shows: that `x-data` must receive a JavaScript *object literal* (`{ key: value }`)
to create named reactive properties. A string, number, or array works as a data
source only if you access its built-in properties.

To find it: open DevTools and inspect the element. Check what `x-data` evaluates
to. Replace `x-data="'hello'"` with `x-data="{ message: 'hello' }"` so that
`message` is a named, reactive property.

</details>

## Show and hide an error message {: #alpine-xiftemplate}

Open the page and click "Trigger Error" several times.
Does the error message appear and disappear?

[% inc xiftemplate.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is putting `x-if` on a `<div>` instead of a `<template>` element.
Alpine requires `x-if` to be on a `<template>` tag, because `<template>` has
no rendered output of its own — it is a pure placeholder. When `x-if` appears
on any other element, Alpine silently ignores it and the content is always shown.

Shows: the distinction between `x-if` (which adds and removes elements from the DOM
entirely, and requires `<template>`) and `x-show` (which toggles `display: none` on
any element).

To find it: open the console. Alpine logs a warning when `x-if` is misused.
Replace `<div x-if="hasError">` with `<template x-if="hasError"><div>...</div></template>`.

</details>

## Mirror text input in real time {: #alpine-modelbind}

Open the page and type in the input field.
Does the paragraph below update as you type?

[% inc modelbind.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `x-bind:value` instead of `x-model`. `x-bind:value` only sets the
input's `value` attribute from the reactive property — it does not listen for changes.
When the user types, the input's visual content changes, but no event updates
`message` in the Alpine component. The binding runs only one way: state to input.

Shows: the difference between `x-bind:value` (one-way, state → element) and `x-model`
(two-way, state ↔ element). `x-model` is shorthand for `x-bind:value` *plus*
`@input="message = $event.target.value"`.

To find it: type in the input and check `message` in the Alpine devtools or the
console. If it stays empty, the input is not sending updates back. Replace
`x-bind:value="message"` with `x-model="message"`.

</details>

## Show an input and move focus to it {: #alpine-nexttick}

Open the page and click "Edit".
Does the cursor appear inside the input field?

[% inc nexttick.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `$refs.field.focus()` in the same synchronous tick as the
`x-show` update. When `editing = true` runs, Alpine schedules the DOM update
for the next microtask — the element is still hidden when `focus()` is called
immediately after. Browsers refuse to focus hidden elements, so the call silently
does nothing.

Shows: Alpine's batched, asynchronous DOM updates and `$nextTick`, which delays a
callback until after Alpine has finished applying all pending changes to the DOM.

To find it: add `console.log($refs.field.style.display)` before the focus call.
If it logs `"none"`, the element is still hidden. Change the click handler to
`editing = true; $nextTick(() => $refs.field.focus())`.

</details>

## Load data from the server on startup {: #alpine-asyncinit}

Start the server, open the page, and wait a moment.
Does a greeting appear, or does the paragraph show the fallback message?

[% inc asyncinit.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `loadGreeting` is a named global function. Inside a named function,
bare identifiers like `greeting` refer to the surrounding JavaScript scope — in this
case, the global (`window`) scope. Alpine evaluates `x-init="loadGreeting()"` in its
component scope, but once execution enters the named function body, that scope is gone.
The assignment `greeting = data.message` creates or updates `window.greeting`, not the
component's reactive `greeting` property, so Alpine never sees the change.

Shows: how Alpine's scope injection works only inside expression strings — not inside
called function bodies — and why `x-init` expressions that use component properties
should be written inline or receive `this` explicitly.

To find it: add `console.log(window.greeting)` inside `loadGreeting` after the fetch.
If it shows the message, the assignment hit the global scope. Fix the handler by
writing it inline so Alpine's scope applies:

```
x-init="async () => { const r = await fetch('/api/greeting'); greeting = (await r.json()).message; }"
```

</details>

## Display a count from a shared store {: #alpine-storeorder}

Open the page and check the browser console.
Does a number appear next to "Items in cart"?

[% inc storeorder.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `Alpine.store('cart', { count: 0 })` is never called, so
`$store.cart` is `undefined`. When the template tries to read `$store.cart.count`,
JavaScript throws `TypeError: Cannot read properties of undefined`, the component
fails to render, and the console shows an error.

Shows: that `Alpine.store` must be registered before Alpine initializes the
components that use it. The correct place to register a store is inside the
`alpine:init` event listener, which fires before Alpine processes any components.

To find it: open the console and read the error. Uncomment the
`Alpine.store('cart', { count: 0 })` line inside the `alpine:init` listener.

</details>

## Remove items from a list {: #alpine-forkey}

Open the page, type something in the second row's input, then click Delete
next to the first item. Which row's typed text disappears?

[% inc forkey.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `:key` binding on `x-for`. Without a key, Alpine matches
old DOM nodes to new data items purely by position. After the first item is removed,
every remaining item shifts up by one position. Alpine reuses the existing DOM nodes
in order rather than creating new ones, which means the `<input>` that belonged to
the second item stays in place but is now labeled as the first item. Any typed
content appears to have moved to the wrong row.

Shows: why `:key` matters and how Alpine uses it to match DOM nodes to data items
by identity rather than by index, allowing it to move or remove the correct node.

To find it: type in the second input, delete the first item, and watch which input
retains the typed value. Add `:key="item"` to the `<template>` tag (or use a unique
id if items can repeat) so Alpine tracks each DOM node correctly.

</details>

## Increment a counter using an external object {: #alpine-globalstate}

Open the page and click Increment several times.
Does the counter change?

[% inc globalstate.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `config.count++`. When Alpine sees `x-data="config"`, it copies the
properties of `config` into a new reactive proxy and uses that proxy to drive the
template. Clicking the button updates `config.count` on the original plain object,
which is no longer connected to Alpine's proxy. The proxy still holds the old value,
so the display never changes.

Shows: that `x-data` takes a snapshot of its argument's properties at initialization
time. Mutations to the original object after that point are invisible to Alpine.
Reactive updates must go through the proxy — meaning you use the bare property name
(`count++`) inside an Alpine expression, not a reference to the external object.

To find it: add `console.log(config.count)` to the click handler. If it increments
but the display doesn't, the external object and the proxy have diverged. Change
`config.count++` to `count++`.

</details>

## Close a panel by pressing Escape {: #alpine-keyboardtarget}

Open the page, click somewhere inside the panel, and press Escape.
Does the panel close?

[% inc keyboardtarget.html scrub="\s*(//|<!--).*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing `@keydown.escape` on a `<div>` that has no `tabindex` attribute.
Keyboard events are dispatched only to elements that can receive focus. Plain `<div>`
elements are not focusable by default, so they never appear in the keyboard event
path and the `@keydown` listener never fires, no matter how many times you press Escape.

Shows: the connection between focusability and keyboard events, and two ways Alpine
provides to listen for window-level keyboard events:

-   Add `tabindex="0"` to the `<div>` to make it focusable, then call `.focus()` when
    the panel opens.
-   Replace `@keydown.escape` with `@keydown.window.escape`, which attaches the listener
    to the window so it fires regardless of which element has focus.

To find it: open DevTools, click inside the panel, and check the Elements panel to
see if the `<div>` is focused (a blue outline or the `:focus` pseudo-class). If it
isn't focusable, keyboard events skip it.

</details>
