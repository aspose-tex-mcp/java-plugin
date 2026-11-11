"""TeX/Java documentation theme policy; owned by this plugin."""

import re

from dataclasses import replace

from adcs_tex_java.gist_examples import UNAVAILABLE_RE, expand
from adcs_tex_java.hugo_parser import HugoMarkdownParser, HugoParseWarning

_HIGHLIGHT_RE = re.compile(
    r'{{[<%]\s*highlight\s+["\']?([\w#+-]+)["\']?[^{}]*[>%]}}(.*?){{[<%]\s*/highlight\s*[>%]}}',
    re.S,
)
# The Java documentation copied many examples from .NET pages and kept the
# ``csharp`` highlight label. Relabel only blocks that are evidently Java and
# show no C# idiom; genuine C# (release-note API diffs), PHP-via-Java, shell
# and template snippets keep their declared label.
_JAVA_EVIDENCE = re.compile(
    r"\b(?:String\[\]|System\.out\.|import\s+com\.aspose|throws\s+Exception)"
    r"|\.(?:get|set|save|insert|append|execute|run)[A-Z]?\w*\(.*\);\s*$",
    re.M,
)
_CSHARP_EVIDENCE = re.compile(
    r"\bvar\s|\.(?:Save|Execute|Insert|Append)\w*\(|\busing\s|\bstring\b|=>|\bforeach\b"
    r"|\.Count\b|///\s*<summary>|\{\s*get;"
)


def fence_language(declared: str, code: str) -> str:
    language = declared.casefold()
    if language in {"csharp", "c#", "cs"} and _JAVA_EVIDENCE.search(code) and not (
        _CSHARP_EVIDENCE.search(code)
    ):
        return "java"
    return declared


# TeX documentation theme markup with no content of its own:
# ``{{<section overview>}}`` marks a layout section, ``{{< emoticons/tick >}}``
# is a check mark in the supported-formats table, and ``{{lang.url-fragment}}``
# is a site-language placeholder inside root-relative links (``/tex/{{...}}java/``).
_SECTION_RE = re.compile(r"^[ \t]*{{<\s*section\b[^{}]*>}}[ \t]*\n?", re.M)
_TICK_RE = re.compile(r"{{<\s*emoticons/tick\s*>}}")
_LANG_FRAGMENT_RE = re.compile(r"{{\s*lang\.url-fragment\s*}}")


def theme_markup(text: str) -> str:
    text = _SECTION_RE.sub("", text)
    text = _TICK_RE.sub("✓", text)
    return _LANG_FRAGMENT_RE.sub("", text)


def extract(request):
    text = request["raw_markdown"].removeprefix("﻿")
    text = theme_markup(expand(text))
    # Examples recorded as absent upstream: drop the marker, keep a warning
    # (front-matter-relative line numbers are approximate for these markers).
    unavailable = [
        (text.count("\n", 0, match.start()) + 1, match[1])
        for match in UNAVAILABLE_RE.finditer(text)
    ]
    text = UNAVAILABLE_RE.sub("", text)
    # Convert paired Hugo highlight shortcodes to fenced examples before parsing.
    # Unknown shortcodes retain the parser's explicit warnings.
    text = _HIGHLIGHT_RE.sub(
        lambda match: "```" + fence_language(match[1], match[2]) + match[2] + "```",
        text,
    )
    page = HugoMarkdownParser().parse_document(
        **{
            key: request[key]
            for key in (
                "repo_id",
                "source_path",
                "source_kind",
                "product_id",
                "product_family",
                "relative_repo_path",
                "layout_detection",
            )
        },
        raw_markdown=text,
    )
    if not unavailable:
        return page
    warnings = tuple(
        HugoParseWarning(
            code="GIST_EXAMPLE_UNAVAILABLE",
            message=f"Gist example {reference} is not present in the pinned Gist revision.",
            line_hint=line,
        )
        for line, reference in unavailable
    )
    return replace(page, parse_warnings=page.parse_warnings + warnings)
