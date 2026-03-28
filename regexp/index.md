# Regular Expressions

## Validate phone numbers in a contact list {: #regexp-phone}

This function is supposed to accept only strings that are phone numbers and
reject everything else. Call it with `"call 555-867-5309 now"` and with
`"555-867-53090000"`. Do both results match your expectations?

[% inc phone.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `re.search` instead of `re.fullmatch`. `re.search` finds the
pattern *anywhere* in the string, so a sentence that contains a phone number
passes the check even though it is not a phone number, and a string of extra
digits such as `"555-867-53090000"` also passes because the pattern matches
the first ten digits and ignores the rest.

Shows: the difference between `re.search` (match anywhere), `re.match`
(match at the start), and `re.fullmatch` (match the entire string), and
why validation functions almost always need `re.fullmatch`.

To find it: print `re.search(PATTERN, "call 555-867-5309 now").span()`.
The span `(9, 21)` shows the match starts at character nine, not character
zero, confirming that the match is embedded inside the string rather than
being the whole string. Replace `re.search` with `re.fullmatch` so that only
strings that are *entirely* a phone number pass.

</details>

## Detect timestamps in log entries {: #regexp-access}

This function is supposed to return `True` for any log line that contains a
date. Call it with `"ERROR on 2024-01-15: disk full"`. Does it return the
result you expect?

[% inc access.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `re.match` instead of `re.search`. `re.match` only checks
whether the pattern appears at the *start* of the string, so a date that
appears after other text is never found.

Shows: `re.match` is not a whole-string check; it is an anchored-at-the-start
check. The complement to `re.match` for finding a pattern anywhere is
`re.search`.

To find it: call `re.match(PATTERN, "ERROR on 2024-01-15: disk full")` and
print the result. It returns `None` because `"ERROR"` does not match
`\d{4}-\d{2}-\d{2}`. Replace `re.match` with `re.search` to check anywhere
in the string.

</details>

## Count action items in source code {: #regexp-comments}

Run this script and compare the count it prints to the number of action items
you can see in the source string. Do the counts agree?

[% inc comments.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the pattern `# TODO:` is case-sensitive, so `# todo:` and
`# Todo:` are not matched, and the function reports one instead of three.

Shows: Python's `re` module is case-sensitive by default, and the same word
spelled with different capitalisation is treated as a different pattern.

To find it: call `re.findall(r"# TODO:", "# todo: example")` and observe
that it returns an empty list. Add `re.IGNORECASE` as a second argument to
`re.findall` to make the match case-insensitive.

</details>

## Find headings in a document {: #regexp-headings}

Run this script and count the Markdown headings in the document string by
hand. Does the function find all of them?

[% inc headings.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `^` without `re.MULTILINE` matches only the very start of the
entire string, not the start of each line. The first heading `"# Introduction"`
is found because it appears at position zero; all subsequent headings are
missed because they begin after a newline character, not at the string's start.

Shows: in Python's `re` module, `^` and `$` match the start and end of the
*string* by default. Pass `re.MULTILINE` to make them match the start and end
of each *line* instead.

To find it: print `bool(re.search(r"^## Background", doc))` — it returns
`False`. Then print `bool(re.search(r"^## Background", doc, re.MULTILINE))`
— it returns `True`. Add `re.MULTILINE` to the `re.findall` call to fix the
function.

</details>

## Find error messages in a log file {: #regexp-logentry}

Run this script on the sample log string. The exception message spans more
than one line. Does the function find it?

[% inc logentry.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the `.` metacharacter does not match newline characters by
default, so the pattern never bridges the line break between `"ValueError"`
and `"END"`.

Shows: `.` matches any character *except* a newline unless `re.DOTALL` is
passed. This is the source of many silent failures when patterns are applied
to multi-line strings.

To find it: print `re.search(r".", "\n")` — it returns `None`, confirming
that `.` does not match `\n`. Pass `re.DOTALL` as a third argument to
`re.findall` to make `.` match newlines and let the pattern span lines.

</details>

## Recognize column names in a CSV header {: #regexp-columns}

Run this script and compare the list it prints to the column names in the
header string. Which columns are missing from the output?

[% inc columns.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `re.compile` is called without `re.IGNORECASE`, so the
compiled pattern only matches lowercase letters. The header uses title-case
column names (`"Name"`, `"Email"`, `"Phone"`), none of which match the
all-lowercase pattern.

Shows: flags must be supplied at compile time when using `re.compile`; they
cannot be added later. A compiled pattern without a flag behaves differently
from one compiled with it.

To find it: call `COLUMN_RE.search("Name")` and observe it returns `None`.
Then call `re.search(r"name", "Name", re.IGNORECASE)` and observe it returns
a match. Pass `re.IGNORECASE` as a second argument to `re.compile` to fix
the pattern.

</details>

## Extract prices from a web page {: #regexp-prices}

Run this script and count the `<amount>` tags in the HTML string by hand.
Does the function return the same number of prices?

[% inc prices.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `.*` is *greedy*: it matches as many characters as possible.
The pattern `<amount>(.*)</amount>` starts at the first `<amount>` and
expands `.*` until it reaches the *last* `</amount>`, capturing everything in
between — including the middle tag and the tax field — as a single match.

Shows: greedy quantifiers extend as far right as possible; lazy quantifiers
(`.*?`) extend only as far as necessary. Greedy behaviour is the default and
is often wrong when the surrounding delimiters appear more than once.

To find it: print the single item returned by `extract_amounts` and observe
that it contains the entire middle of the string. Replace `.*` with `.*?` to
make the quantifier lazy, so each `<amount>` tag matches only up to its own
`</amount>`.

</details>

## Filter empty attributes from an HTML element {: #regexp-attrs}

Run this script and inspect the list it returns. Should an empty `id`
attribute be included in that list?

[% inc attrs.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `\w*`, which matches *zero or more* word characters. An empty
`id=""` attribute satisfies `\w*` (with zero characters), so the empty string
`""` is captured and appears in the results.

Shows: `*` and `+` are easy to confuse. Use `\w+` when the match must contain
at least one character and `\w*` only when an empty match is acceptable.

To find it: test `bool(re.search(r"\w*", ""))` — it returns `True`, confirming
that `\w*` accepts an empty string. Replace `\w*` with `\w+` in the pattern to
require at least one word character inside the attribute value.

</details>

## Validate postal codes in an address database {: #regexp-postal}

Run this script and check which strings it identifies as ZIP codes. Examine
the input and the output side by side.

[% inc postal.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `\d{4}`, which matches exactly four digits, but US ZIP codes
contain five. None of the valid ZIP codes in the input are found, and the
four-digit apartment number `4201` is matched instead.

Shows: off-by-one errors appear in `{n}` quantifiers as well as in loop
indices. Always verify the exact length required by the format you are
matching.

To find it: evaluate `bool(re.search(r"\d{4}", "90210"))` — it returns
`True`, but only because `\d{4}` matches the first four digits of the five-
digit ZIP code, not all five. Change `{4}` to `{5}` so the pattern requires
exactly five digits.

</details>

## Filter server addresses from a configuration {: #regexp-network}

This function is supposed to accept only valid IP address strings. Call it
with `"192X168X1X1"`. Does it reject that input?

[% inc network.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the dots separating the octets are not escaped. In a regular
expression, `.` matches any character, so `\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}`
accepts any single character between the digit groups — including `X`.

Shows: literal characters that are also regex metacharacters (`. * + ? [ ] { }
( ) ^ $ | \`) must be escaped with a backslash to match themselves.

To find it: test `bool(re.fullmatch(r".", "X"))` — it returns `True`, showing
that an unescaped dot accepts `"X"`. Replace each `.` in the pattern with `\.`
so only a literal period is accepted between the digit groups.

</details>

## Remove markup from user submissions {: #regexp-htmlstrip}

Run this script and look at what `strip_tags` returns. Does the HTML it
receives end up as plain text?

[% inc htmlstrip.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the character class `[<>]`, which matches only the characters `<`
and `>`. Because normal HTML tags contain letters, not angle brackets, the
pattern `<[<>]+>` never matches any real tag, and nothing is removed.

Shows: inside a character class, `^` at the very start *negates* the class.
`[<>]` means "either `<` or `>`", while `[^<>]` means "any character that
is *not* `<` or `>`".

To find it: test `bool(re.search(r"<[<>]+>", "<b>"))` — it returns `False`,
because the character `b` is not in `[<>]`. Change `[<>]` to `[^<>]` so the
pattern matches any sequence of non-bracket characters between the two angle
brackets.

</details>

## Classify links by protocol {: #regexp-schemes}

Run this script and check the scheme reported for the HTTPS URL. Does the
label match the URL?

[% inc schemes.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `"http"` appears before `"https"` in the alternation. Regular
expression alternation is ordered: the engine tries each alternative from left
to right and stops at the first match. Because `"http"` is a prefix of
`"https"`, it matches the first four characters of any HTTPS URL and the
engine never tries the longer alternative.

Shows: when one alternative is a prefix of another, put the longer one first.
`r"https|http"` or the equivalent shorthand `r"https?"` both work correctly.

To find it: evaluate `re.match(r"http|https", "https://example.com").group(0)`
— it returns `"http"`, not `"https"`. Swap the order to `r"https|http"` or
rewrite the pattern as `r"https?"`.

</details>

## Count a word in a paragraph {: #regexp-wordcount}

Run this script and count the standalone occurrences of `"log"` in the text
by hand. Does the function return the same number?

[% inc wordcount.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the pattern has no word boundaries, so `"log"` matches inside
`"login"`, `"dialog"`, and `"catalog"` as well as the standalone word, giving
a count of four instead of one.

Shows: `\b` is a zero-width assertion that matches the position between a word
character and a non-word character. Use `r"\blog\b"` to match the whole word
only.

To find it: print `re.findall(r"log", text)` and examine the list — you will
see four items. Then print `re.findall(r"\blog\b", text)` and see only one.
Add `\b` before and after the word in the pattern.

</details>

## Reformat names in a mailing list {: #regexp-roster}

Run this script and check whether the output names are in "First Last" order.
Are they?

[% inc roster.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the replacement string `r"\1 \2"` keeps the groups in their
original order. Group 1 captures the last name (everything before the comma)
and group 2 captures the first name, so `r"\1 \2"` produces "Last First"
rather than "First Last".

Shows: groups are numbered left to right by opening parenthesis. Drawing a
quick table of which group captures which field before writing the replacement
string prevents this error.

To find it: add a `print` statement inside `reformat_name` to show
`re.search(PATTERN, name).groups()` for the first input — it returns
`('Smith', 'Alice')`, confirming that group 1 is the last name. Change the
replacement to `r"\2 \1"` to put the first name before the last name.

</details>

## Redact sensitive fields in a report {: #regexp-redact}

Run this script and inspect the `repr()` of the result. Are the sensitive
labels preserved in the output as expected?

[% inc redact.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the replacement string `"\1: [redacted]"` is a regular Python
string, not a raw string. Python's string parser converts `\1` to the SOH
control character (the byte with value 1) before `re.sub` ever sees it. The
`re` module then interprets that byte as a backreference, but the result is a
garbled character instead of the matched label.

Shows: replacement strings for `re.sub` that contain backreferences must be
raw strings (prefix `r`) so Python does not interpret the backslash before
`re.sub` processes it.

To find it: print `repr("\1")` — it shows `'\x01'`, confirming the string
contains a control character, not a backslash followed by `1`. Change the
replacement to `r"\1: [redacted]"` to pass the literal two-character sequence
`\1` to `re.sub`.

</details>

## List settings from a configuration string {: #regexp-settings}

Run this script and look at the values it finds. What is missing from each
item in the list?

[% inc settings.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that a capturing group `(\w+)` is present in the pattern. When
`re.findall` finds a pattern that contains one or more groups, it returns the
*group contents* rather than the full match strings. Here every item in the
result is just the value portion, with the key and the `=` sign missing.

Shows: `re.findall` has two modes — when there are no groups it returns a list
of full match strings; when there is at least one group it returns a list of
the group contents (or a list of tuples when there are multiple groups).

To find it: evaluate `re.findall(r"\w+=(\w+)", "a=1 b=2")` — it returns
`['1', '2']`, not `['a=1', 'b=2']`. Remove the parentheses from the pattern
to get full matches, or capture both key and value in separate groups and
handle the tuples in the calling code.

</details>

## Pull dates from a report {: #regexp-years}

Run this script and examine what it prints. Are the values in the list complete
dates, or something shorter?

[% inc years.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a capturing group around the year portion of the pattern. Because
the group exists, `re.findall` returns only what the group captured — the
four-digit year — rather than the full date string that matched.

Shows: even a single capturing group changes what `re.findall` returns. Use a
non-capturing group `(?:...)` when grouping is needed for structure but the
full match is what you want to collect.

To find it: compare `re.findall(r"(\d{4})-\d{2}-\d{2}", text)` with
`re.findall(r"\d{4}-\d{2}-\d{2}", text)` using the same input. The first
returns years; the second returns full dates. Either remove the parentheses or
replace them with `(?:...)` to restore the full-match behaviour.

</details>

## Check password strength {: #regexp-strength}

Run this script. Which passwords does it mark as strong? Are any of those
passwords actually weak by the stated rules?

[% inc strength.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the pattern checks for at least one digit using
`(?=.*\d)` but never checks for an uppercase letter. The intended rule
requires *both* a digit and an uppercase letter, so `"password1"` (no
uppercase) and `"12345678"` (no letter) both pass incorrectly.

Shows: a lookahead `(?=...)` is a zero-width assertion — it checks a condition
without consuming characters. Each independent requirement needs its own
lookahead; a single lookahead can only verify one condition at a time.

To find it: evaluate `bool(re.fullmatch(PATTERN, "password1"))` — it returns
`True` even though `"password1"` contains no uppercase letter. Add a second
lookahead `(?=.*[A-Z])` immediately after the first to enforce both
requirements: `r"(?=.*\d)(?=.*[A-Z])[A-Za-z\d]{8,}"`.

</details>
