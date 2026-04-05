# HTTP and APIs

## No Status Check Before Parsing {: #web-nostatuscheck}

Run the script and read the error message. What type of error is raised, and which
line causes it? Is the problem in the line that fails or somewhere earlier?

[% inc nostatuscheck.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is calling `.json()` without first checking `r.status_code`. A 404 response
returns an HTML error page, not JSON, so `.json()` raises a `JSONDecodeError` at the
parsing step rather than flagging the real problem, which is the failed request.
Teaches how to check `r.status_code` or call `r.raise_for_status()` before reading
the response body.

</details>

## Form Encoding Instead of JSON {: #web-jsonparam}

Run the script and read the output. What content type does the server report
receiving? What content type did you intend to send?

[% inc jsonparam.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `data=` instead of `json=` in the POST call. `data=` sends a
form-encoded body with `content-type: application/x-www-form-urlencoded`, while
most APIs expect `json=` which sends a JSON body with `content-type:
application/json`. Teaches the difference between these two keyword arguments and
why the server may silently reject or misparse a request sent with the wrong
encoding.

</details>

## Special Characters in Query Parameters {: #web-urlparam}

Run the script and read the output. How many query parameters did the server receive?
How many did the code intend to send?

[% inc urlparam.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is embedding a value that contains `&` directly in an f-string URL. The
ampersand is interpreted as a query-string separator, so the server receives
`category=books` and a bare key `games` instead of `category=books&games`. Teaches
how to pass query parameters as a `params=` dict so the HTTP client encodes special
characters correctly.

</details>

## Missing Pagination {: #web-nopaginate}

Run the script and compare the number of records retrieved to the total available.
What field in the response tells you that more data exists?

[% inc nopaginate.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is fetching only the first page and ignoring the `next_page` field in the
response. No error is raised; the script silently processes a fraction of the
available data. Teaches how to recognize and follow pagination cursors and why APIs
return data in pages rather than all at once.

</details>

## Disabled Request Timeout {: #web-notimeout}

Run the script. Does it return promptly? How long does it wait before producing
output?

[% inc notimeout.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is passing `timeout=None`, which disables all timeouts and causes the call to
wait indefinitely for a slow or unresponsive server. Teaches the difference between
httpx's default timeout and `timeout=None`, and how to set an explicit
`httpx.Timeout` to bound how long a request may take.

</details>

## Checking for 200 Instead of Any 2xx {: #web-created}

Run the script. What status code does the server return? What does the script print?
Is the request actually successful?

[% inc created.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is comparing `r.status_code == 200` when a successful POST returns
`201 Created`. The response is treated as a failure even though the resource was
created. Teaches the range of 2xx status codes, when each is used, and how to use
`r.is_success` to accept any successful response.

</details>

## Retrying Without Reading Retry-After {: #web-ratelimit}

Run the script and look at the status code and headers on each attempt. What does
the `Retry-After` header contain? Does the script wait before retrying?

[% inc ratelimit.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is retrying immediately after a 429 Too Many Requests response without
reading the `Retry-After` header. Each retry is rejected for the same reason and the
script loops without ever succeeding. Teaches what 429 means, how to detect it, and
how to wait the server-specified duration before the next attempt.

</details>

## PUT Replaces Instead of Updates {: #web-putpatch}

Run the script and compare the resource state before and after the PUT request.
Which fields changed, and which fields were you expecting to keep?

[% inc putpatch.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using PUT with a partial body. PUT replaces the entire resource with
the request body, so any field not included in the request is wiped. Teaches the
semantic difference between PUT (full replacement) and PATCH (partial update), and
why sending only the fields you want to change requires PATCH.

</details>

## API Key in URL Query String {: #web-tokenurl}

Run the script and read the output. In which part of the request does the API key
appear? What would a server log entry look like?

[% inc tokenurl.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is placing the API key in the URL query string. Query strings are recorded
in server access logs, browser history, and any intermediate proxies, so the secret
is exposed in plaintext. Teaches how to pass credentials in an `Authorization`
header instead, where they are kept out of logs and not cached by browsers.

</details>

## POST Body Lost After Redirect {: #web-postredirect}

Run the script and read the output. What HTTP method reached the final endpoint?
What happened to the request body that was sent to `/submit`?

[% inc postredirect.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is following a 302 redirect from a POST request. HTTP convention changes the
method from POST to GET when following a 302, so the request body is silently
dropped and the final endpoint receives an empty GET request. Teaches how redirects
interact with request methods, and how to detect this by inspecting the method and
body at the redirected URL.

</details>
