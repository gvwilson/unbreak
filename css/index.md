# CSS

CSS controls how HTML elements look on screen.
Its rules seem simple at first—select an element, set some properties—but a handful of
non-obvious behaviors trip up almost every developer at least once.
Open each example directly in a browser to see the problem in action.

## Change the color of a heading {: #css-fontcolor}

Open the page. The heading should be red. Is it?

[% inc fontcolor.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `font-color`, which is not a valid CSS property. The correct property is
`color`. When a browser encounters a property name it does not recognize, it discards
the entire declaration silently—no error appears on the page or in the console unless
you check the DevTools Styles panel.

Shows: that CSS ignores unknown property names without warning, and that the property
for text color is `color`, not `font-color`.

To find it: open DevTools, select the `<h1>`, and look at the Styles panel. The
`font-color: tomato` declaration will have a yellow warning triangle or a strikethrough
indicating it is invalid. Change `font-color` to `color`.

</details>

## Make a heading larger {: #css-unitless}

Open the page. The heading should be noticeably larger than the paragraph below it.
Is it?

[% inc unitless.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing unit. `font-size: 48` is invalid—CSS requires a unit such as
`px`, `em`, or `rem` for length values (zero is the only exception). The browser
discards the invalid declaration and falls back to the default heading size.

Shows: that most CSS length values require an explicit unit and that `48` and `48px`
are completely different things to the browser.

To find it: open DevTools, select the `<h1>`, and look at the Styles panel. The
`font-size: 48` line will be flagged as invalid. Change it to `font-size: 48px`.

</details>

## Style an error message {: #css-classmatch}

Open the page. The message should have a red background and white text. Does it?

[% inc classmatch.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a mismatch between the selector and the HTML. The CSS targets `.warning`
but the element has `class="error"`. CSS class selectors are case-sensitive and must
match exactly. No element in the document has the class `warning`, so the rule applies
to nothing.

Shows: how to connect CSS rules to HTML elements via class names, and that a missing
style is often a typo in either the selector or the HTML attribute.

To find it: compare the selector in the stylesheet to the `class` attribute in the
HTML. Either change `.warning` to `.error` in the CSS, or change `class="error"` to
`class="warning"` in the HTML.

</details>

## Style a button with several properties {: #css-semicolon}

Open the page. The button should have white text and visible padding around it.
Does it?

[% inc semicolon.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing semicolon after `color: white`. CSS declarations inside a rule
are separated by semicolons. When the semicolon is absent, the parser treats the next
line as a continuation of the same declaration. `color: white padding: 10px 20px` is
not a valid value, so the browser discards the entire declaration—losing both the
`color` and the `padding`.

Shows: how a single missing semicolon can silently drop multiple declarations and why
CSS parse errors do not stop the rest of the stylesheet from loading.

To find it: open DevTools, select the button, and look at the Styles panel. Both
`color` and `padding` will be absent or flagged. Add the missing semicolon after
`color: white`.

</details>

## Set the width of a label {: #css-inline}

Open the page. The blue label should be 200px wide. Is it wider than its text?

[% inc inline.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `<span>` is an inline element. Inline elements flow with text and
ignore `width` and `height` declarations. The label is exactly as wide as its content
regardless of what the CSS says.

Shows: the inline/block distinction and that `width` only affects block-level or
replaced elements (such as `<img>`).

To find it: in DevTools, select the `<span>` and look at the box model diagram. The
width will equal the text width, not 200px. Add `display: inline-block` or
`display: block` to the `.label` rule to make `width` take effect.

</details>

## Add a background image to a panel {: #css-background}

Open the page. The panel should have a blue background (shown when the image is
missing). Is it blue?

[% inc background.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is declaration order. The `background` shorthand property sets every
background sub-property at once, including `background-color`, resetting it to
`transparent`. Because `background` appears after `background-color` in the rule,
it overwrites the blue color. The image URL does not exist, and the fallback color
is now transparent rather than blue.

Shows: that `background` is a shorthand that resets all background sub-properties,
and that rule order within a block matters.

To find it: in DevTools, look at the computed `background-color` for the panel. It
will be transparent. Either move `background-color` after the `background` line, or
include the color directly in the shorthand: `background: url("...") no-repeat center
center steelblue`.

</details>

## Hide a notice without moving other content {: #css-visibility}

Open the page. Compare where the paragraph sits relative to where it would be if the
notice were visible. Did the paragraph move up?

[% inc visibility.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `display: none` when `visibility: hidden` is needed. `display: none`
removes the element from the layout entirely—other elements flow in as if it were not
there. `visibility: hidden` hides the element visually but reserves its space, so
surrounding elements do not shift.

Shows: the difference between `display: none` (removes from flow) and `visibility:
hidden` (invisible but still occupies space).

To find it: in DevTools, toggle `display: none` off. The notice reappears and the
paragraph drops back to its original position, confirming the layout was collapsing.
Change `display: none` to `visibility: hidden` to hide the notice while preserving
the layout.

</details>

## Center a button on the page {: #css-textalign}

Open the page. The button should be centered horizontally on the page. Is it?

[% inc textalign.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is applying `text-align: center` to the button itself. `text-align` controls
the alignment of inline content—text and inline elements—inside the element it is
applied to. On the button, it centers the label text within the button's box. It does
nothing to position the button on the page.

Shows: that `text-align` affects content inside an element, not the element's position
in its parent, and that centering a block-level element requires a different technique.

To find it: look at the button in DevTools. The text inside is centered, but the button
stretches edge to edge. Move `text-align: center` to the parent element (e.g., `body`
or a wrapper `<div>`). A block-level child inherits the alignment hint and centers
within its parent.

</details>

## Center a card horizontally {: #css-marginauto}

Open the page. The blue card should be centered with equal space on each side.
Is it?

[% inc marginauto.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `width`. `margin: 0 auto` centers a block element by dividing
leftover horizontal space equally between the left and right margins. But a block
element without an explicit width expands to fill its container entirely, leaving no
leftover space to distribute. The card is full-width and `auto` resolves to zero on
both sides.

Shows: that `margin: 0 auto` only works when the element is narrower than its
container, which requires an explicit width.

To find it: in DevTools, look at the computed `margin-left` and `margin-right`—both
will be 0. Add `width: 300px` (or any value less than the container width) to `.card`
so the browser has remaining space to divide equally.

</details>

## Color a link differently on hover {: #css-hoverorder}

Click the link to visit it, then come back and hover over it. Does it turn red?

[% inc hoverorder.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is rule order. All three selectors (`a:hover`, `a:visited`, `a:link`) have
the same specificity, so the browser uses source order as a tiebreaker—the last
matching rule wins. For a visited link, both `a:hover` and `a:visited` match when
the cursor is over it. Because `a:visited` appears after `a:hover` in the stylesheet,
it always wins and the hover color never shows. The correct order is
`:link`, `:visited`, `:hover`, `:active`—often remembered as LVHA.

Shows: how the CSS cascade uses source order when specificity is equal, and why link
pseudo-classes must be declared in LVHA order.

To find it: reorder the rules so `a:link` comes first, then `a:visited`, then
`a:hover`. With that order, `:hover` appears later and overrides `:visited` when
the cursor is present.

</details>

## Fit a panel inside a container {: #css-boxmodel}

Open the page. The blue panel should sit entirely within the grey container.
Does it, or does it overflow to the right?

[% inc boxmodel.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `box-sizing: content-box`, which is the default. When `width: 100%` is set,
the browser assigns 100% of the container's width to the content area alone. Padding is
then added on top, making the element wider than the container—300px content + 20px left
padding + 20px right padding = 340px total.

Shows: the CSS box model and the difference between `content-box` and `border-box`.

To find it: open DevTools, select the panel, and look at the box model diagram in the
Computed tab. The total rendered width will exceed the container's width. Add
`box-sizing: border-box` to the `.panel` rule so that padding is included inside the
declared width rather than added to it.

</details>

## Override a color in a stylesheet {: #css-specificity}

Open the page. Both elements use the `.highlight` class. Are they both red?

[% inc specificity.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a specificity conflict. The selector `nav.highlight` targets an element type
plus a class, giving it specificity (0,1,1). The later rule `.highlight` is class-only,
specificity (0,1,0). CSS resolves conflicts by specificity first and source order second,
so the less-specific later rule loses to the more-specific earlier rule even though it
appears afterward in the file.

Shows: how the browser calculates specificity and why rule order alone does not determine
which style wins.

To find it: in DevTools, click the `<nav>` element and examine the Styles panel. The
`.highlight { color: red }` rule will be shown with a strikethrough, indicating it was
overridden. To fix it, either change `.highlight` to `nav.highlight, .highlight` or
restructure the stylesheet so both elements share a single rule without the extra type
selector.

</details>

## Add space between sections {: #css-collapse}

Open the page. Section Two has `margin-top: 60px` and Section One has
`margin-bottom: 20px`. Measure the gap. Is it 80px?

[% inc collapse.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is margin collapsing. When two block elements are adjacent siblings, their
vertical margins do not add up—they collapse into a single margin equal to the larger
of the two values. The gap between Section One and Section Two is 60px (the larger
margin), not 80px (the sum).

Shows: vertical margin collapsing between adjacent siblings and why the gap is never
the sum of both margins.

To find it: in DevTools, hover over the gap between sections. The box model overlay
will show only the dominant margin. To get the full 80px gap, convert one of the margins
to padding on the element itself, or add `display: flow-root` to a wrapper to create a
new block formatting context that prevents collapsing.

</details>

## Put a border around an image and caption {: #css-clearfix}

Open the page. The blue border should enclose the image placeholder and the caption.
Does the border appear to wrap them?

[% inc clearfix.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that floated elements are removed from the normal flow. The parent `.card`
has no in-flow children to give it height, so it collapses to zero height (plus
padding). The blue border wraps only the padding, not the floated image or caption.

Shows: how floats interact with parent element height and the classic clearfix problem.

To find it: in DevTools, select `.card` and observe its height is 16px (just padding).
Fix it by adding `overflow: auto` to `.card`, which forces the parent to contain its
floated children. Alternatively, add a clearing element after the floats, or switch to
flexbox or grid.

</details>

## Show a tooltip above an icon {: #css-zindex}

Open the page. The dark tooltip should appear in front of the red banner.
Does it?

[% inc zindex.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `z-index` only works on elements with a `position` value other than
`static`. The `.tooltip` element has no `position` property, so it remains `position:
static` and the `z-index: 100` declaration is ignored entirely. The `.banner` element
has `position: relative`, which enters it into stacking order, so it always paints
on top.

Shows: the requirement that `z-index` needs a non-static `position` to take effect.

To find it: in DevTools, select `.tooltip` and look for `z-index` in the Computed
styles. It will show `auto` (ignored) rather than `100`. Add `position: relative` to
`.tooltip` to activate `z-index` and let the tooltip stack above the banner.

</details>

## Add a decorative bullet to each list item {: #css-pseudo}

Open the page. Each list item should have a gold star to its left.
Do any stars appear?

[% inc pseudo.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a missing `content` property. The `::before` pseudo-element exists in the
DOM only when `content` is present—without it the pseudo-element is not generated at
all, so no star appears regardless of how `color` or `font-size` are set.

Shows: that `::before` and `::after` require `content` to exist, and that `content: ""`
(an empty string) is the minimum needed.

To find it: in DevTools, expand the `<li>` element. No `::before` node will appear in
the tree. Add `content: "\2605"` (the Unicode star character) to the `li::before` rule.
Use `content: ""` as a baseline if you only want to style a generated box with no
visible text.

</details>

## Fill half a page with a colored banner {: #css-pctheight}

Open the page. The blue banner should fill half the grey wrapper.
Is the wrapper visible at all?

[% inc pctheight.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that percentage heights are resolved relative to the parent's computed
height. The `.wrapper` has no explicit height—its height is `auto`, which the browser
calculates from its in-flow content. The browser cannot resolve `50%` of `auto`, so
it treats the child's height as zero. The blue banner has no height and is invisible;
the grey wrapper collapses to nothing as well.

Shows: how percentage heights require an explicit height on the ancestor and why `auto`
breaks the chain.

To find it: in DevTools, select `.banner` and look at its computed height: 0px. To fix
it, give `.wrapper` an explicit height (e.g., `height: 300px`), use viewport units
(`height: 50vh`) on the banner directly, or switch to a flexbox or grid layout.

</details>

## Animate a button color on hover {: #css-transition}

Open the page and hover over the button. Does the background color fade smoothly to
red, or does it snap?

[% inc transition.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `transition: color 0.4s ease` animates the `color` property (text
color), not `background-color`. The hover rule changes `background-color`, which has
no transition declared, so it jumps instantly. Only a text-color change would animate
here, but the hover rule does not change text color, so nothing animates at all.

Shows: how transitions must name the exact CSS property being changed and that `color`
and `background-color` are distinct.

To find it: in DevTools, look at the `.btn` rule and the hover rule side by side. The
transitioned property (`color`) does not match the property changed on hover
(`background-color`). Fix it by changing the transition to `background-color 0.4s ease`
or using `transition: all 0.4s ease` to cover every animated property.

</details>

## Wrap a grid of cards to a new row {: #css-flexwrap}

Open the page. Five cards should wrap onto two rows inside the dashed box.
Do they wrap, or do they overflow to the right?

[% inc flexwrap.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `flex-wrap` defaults to `nowrap`. All flex children are forced onto a
single line regardless of the container's width. When the total minimum size of the
children exceeds the container, they shrink as much as they can and then overflow.

Shows: the default `flex-wrap: nowrap` behavior and why adding `flex-wrap: wrap` is
usually necessary for responsive grid-style layouts.

To find it: open DevTools and select the `.grid` container. In the Layout panel, the
flex wrapping option will show `nowrap`. Add `flex-wrap: wrap` to `.grid` so children
that do not fit on one line flow onto subsequent lines.

</details>

## Add a shadow to a card {: #css-overflow}

Open the page. The white card should have a visible drop shadow.
Can you see any shadow?

[% inc overflow.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `overflow: hidden` on the container. `box-shadow` is painted outside the
element's border-box, in the space between the card and the container's edge. Because
`overflow: hidden` clips everything that extends beyond the container's boundary,
the shadow—which lives in that clipped region—is invisible.

Shows: that `overflow: hidden` clips more than just scrollable content; it also clips
effects such as `box-shadow` and `outline` that paint outside the element's box.

To find it: temporarily set the container to `overflow: visible` in DevTools. The
shadow will reappear immediately. Fix it by removing `overflow: hidden`, switching to
`overflow: clip` (which does not affect shadows in all browsers), or adding enough
`padding` to the container so the shadow falls inside rather than outside it.

</details>

## Make a full-width header with no horizontal scroll {: #css-vw}

Open the page and scroll down until the vertical scrollbar appears.
Does a horizontal scrollbar also appear at the bottom?

[% inc vw.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `width: 100vw`. The `vw` unit measures the full viewport width including
the scrollbar gutter. When a vertical scrollbar is present (about 15–17px wide on
most platforms), the available content area is narrower than `100vw`. The header
overflows by the scrollbar width, which causes the browser to add a horizontal
scrollbar.

Shows: the difference between `100vw` (viewport width) and `100%` (width of the
containing block, which excludes the scrollbar).

To find it: resize the window so no vertical scrollbar is present—the horizontal
scrollbar disappears. Add the scrollbar back—it returns. Replace `width: 100vw` with
`width: 100%` on the header. Because block-level elements default to `width: 100%`,
you can also simply remove the width declaration entirely.

</details>

## Show a dropdown menu on top of a card {: #css-stacking}

Open the page. The dark dropdown should appear in front of the red overlay.
Does it?

[% inc stacking.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `opacity: 0.99` on `.card`. Any `opacity` value less than `1` creates a
new stacking context. Inside that context, the dropdown's `z-index: 200` is compared
only against other descendants of `.card`—not against elements outside it. The `.card`
stacking context as a whole is compared to `.overlay` using `.card`'s z-index, which
is `auto`. `auto` loses to `z-index: 10`, so the entire card (including the dropdown)
is painted behind the overlay.

Shows: how `opacity`, `transform`, `filter`, and a few other properties create new
stacking contexts that trap child z-indices inside them.

To find it: remove `opacity: 0.99` from `.card` in DevTools. The dropdown will jump
in front of the overlay immediately. If you need transparency, apply it only to the
card's background color using `rgba()` rather than the `opacity` property, which
affects all descendants.

</details>

## Set consistent font sizes with relative units {: #css-em}

Open the page. Each nested box uses `font-size: 1.5em`. Should they all be the same
size?

[% inc em.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `em` where `rem` is needed. An `em` is relative to the element's own
computed font size—which is itself resolved from the parent's font size. Each level of
nesting multiplies: 16px × 1.5 = 24px, then 24px × 1.5 = 36px, then 36px × 1.5 =
54px. The text grows exponentially rather than staying constant.

Shows: the difference between `em` (relative to the element's font size, which cascades)
and `rem` (relative to the root element's font size, which stays fixed).

To find it: in DevTools, check the computed `font-size` for each nested element. Each
will be 1.5 times the previous. Replace `em` with `rem` in all three rules so every
element resolves against the root 16px rather than its parent.

</details>

## Highlight every other row in a table {: #css-nthchild}

Open the page. The blue shading should appear on rows 2 and 4 of the data (Banana
and Date). Which rows are actually shaded?

[% inc nthchild.html scrub="\s*\/\*.*BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `tr:nth-child(even)` counts all `<tr>` elements in the table,
including the header row inside `<thead>`. The header is child 1, so the even-numbered
children are header+1 (Apple, child 2), Cherry (child 4), which makes Apple and Cherry
shaded instead of Banana and Date.

Shows: how `:nth-child` counts all siblings of the same parent, not just elements of
the same type, and how `<thead>` and `<tbody>` affect the count.

To find it: add `outline: 2px solid red` to `thead tr` in DevTools and count the rows.
Fix the selector by scoping it to the body rows: `tbody tr:nth-child(even)`. Because
`<tbody>` contains only the data rows, the count starts fresh at Apple (child 1),
making Banana (child 2) and Date (child 4) the even-numbered rows.

</details>
