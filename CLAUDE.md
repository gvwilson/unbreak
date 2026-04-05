# Claude

## Project Overview

-   A tutorial on debugging software that teaches by example.
-   Primary focus is Python, but JavaScript in the browser will be covered as well.
-   Learners are comfortable reading and writing classes and unit tests in Python and JavaScript,
    but have limited understanding of lower-level programming (e.g., C or Rust)
    and limited understanding of threading, networking, containers, and other systems-level issues.
-   Learners use an LLM as a coding assistant but write and debug code themselves.

## Skills

-   Load the `learning-goal` and `learning-opportunities` skills when
    creating lessons.

## Structure

-   Lessons are written in Markdown and compiled to HTML using the `mccole` static site generator.
-   Boilerplate Markdown files:
    -   `CODE_OF_CONDUCT.md`
    -   `CONTRIBUTING.md`
    -   `LICENSE.md`
-   Lesson files:
    -   `README.md`: lesson home page (including table of contents used by `mccole`).
    -   `*/index.md`: lessons (see `README.md` for order).
    -   `docs`: generated HTML.
    -   `_extras/links.md`: Markdown link definitions included in all other Markdown files.
    -   `_static/`: web site assets.
    -   `_templates/`: `jinja2` page template.
-   Custom Python scripts are put in `bin/*.py`.
    -   This project has a `uv` virtual environment, so use `python` rather than `python3` to run commands.

## Build and Test Commands

-   Repeatable actions are saved in `Makefile`.
    -   Run `make` with no arguments to get an up-to-date list of targets.
-   `make site` rebuilds the website from the Markdown files.
-   `make html` checks the generated HTML (but is slow, so should only be used before `git commit`).

## Style Rules

-   `*/index.md` starts with a single H1-level heading (the lesson title).
-   The next line of `*/index.md` may be a subtitle paragraph.
-   Figures, code inclusions, citations, and glossary references are formatted using `mccole` shortcodes.
-   Lessons are written as point-form notes.
-   Do not use **bold** or *italics*.
-   Do not attempt to be funny or offer generic positive feedback to readers.
-   Use `[text][key]` format for external links, and define `key` in `_extras/links.md`.
-   Do not over-use semi-colons or em-dashes.
-   Format mathematics using KaTeX.
-   Each example has:
    -   An H2-level Markdown heading
    -   That heading must have an ID `{: #section-slug}` where `section` is the
        name of the lesson directory and `slug` identifies the particular example.
    -   A short prose description for learners.
    -   Code samples.
    -   An explanation of the bug formatted as shown below.

```
<details class="explanation" markdown="1"><summary>Show explanation</summary>

...text of explanation goes here...

</details>
```

## BUG Comments in Source Files

-   When adding `BUG` comments to source files, every comment line in the block
    must include `BUG` immediately after the comment marker (e.g., `# BUG` or
    `// BUG`).
-   `mccole`'s `scrub` parameter strips lines one at a time using the pattern
    `\s*# BUG.*`. A continuation line that starts with a comment marker without
    `BUG will not be stripped and will appear in the rendered output.
-   Correct:
    ```python
    # BUG: this is wrong because
    # BUG: of this reason
    bad_code()
    ```
-   Incorrect (second line will leak into rendered output):
    ```python
    # BUG: this is wrong because
    # of this reason
    bad_code()
    ```

## Interaction

-   Save a summary of prompts given and actions taken in files in `./log`
    with the date and time of the interaction in UTC as the filename.
-   Run shell commands that do not modify files without asking for permission.
