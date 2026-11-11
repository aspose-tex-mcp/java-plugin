# Aspose.TeX for Java extractor: notes

This package owns discovery, documentation and API Reference extraction,
normalization, semantic chunking and structured API symbol extraction for
**Aspose.TeX for Java** (`plugin_id: aspose.tex.java`, `language: java`). It
started as a copy of the Words/Java plugin and was adapted for
the TeX corpus. Launcher: `python -I worker.py`; installed package:
`python -I -m adcs_tex_java.worker`.

## Source repositories

| Source | Repository | Branch | Prefix | Canonical base |
| --- | --- | --- | --- | --- |
| docs | `aspose-tex-mcp/docs` | `main` | `en/java` | `https://docs.aspose.com/tex/java` |
| apiref | `aspose-tex-mcp/reference` | `master` | `english/java` | `https://reference.aspose.com/tex/java` |

- **Docs:** revision `75002cc2`; the `en/java` content is identical to the
  previously verified `aspose-tex-mcp/aspose-tex-docs` `4443a4a3`. 60 pages:
  developer guide 16, general LaTeX articles 35, getting started 8, FAQ 1.
- **API Reference:** revision `bbfcba7d`. The `english/java` tree was last
  regenerated for 24.9 (September 2024); the Maven release is 26.10. According
  to the Aspose.TeX team, no public API has been added since, so the 24.9
  reference matches the current release.

## Java API Reference model

Same model as Words/Java: one page per type under
`english/java/<package>/<type>/_index.md`; one type row (kind from the leading
declaration) plus one row per constructor, method or field overload with its
own anchor (`#TeXJob-java.lang.String-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-`)
and signature. Chunks never span two members. Package and root pages are
namespace documents without symbols.

Corpus at `bbfcba7d` (24.9): 5 packages, 92 types (69 classes, 13 interfaces,
10 enums), 69 constructors, 428 methods, 47 fields, 636 symbol rows. Enum
constants are fields (`TiffCompression.CompressionLZW`). The TeX reference pages
carry no member examples.

### TeX-specific handling

- **Nested types.** `Size2D.Float` lives in directory `com.aspose.tex/float/`
  with title `Size2D.Float`, declaration
  `public static class Size2D.Float extends Size2D implements Serializable`, and
  front-matter URL `/java/com.aspose.tex/size2d.float/`. The declaration parser
  accepts dotted type names and the FQN is `com.aspose.tex.Size2D.Float`
  (previously `com.aspose.tex.Float`). The live site uses the same
  `size2d.float/` URL.
- **Inline front-matter close.** 12 interface pages write the closing `---` and
  the declaration fence on one line (`---````). The parser recovers the content
  as body and warns `HUGO_FRONT_MATTER_CLOSE_INLINE_CONTENT`; the declaration,
  kind and members are extracted correctly.

## Documentation

- Front-matter `url` values are product-less (`/java/latex-to-pdf/`). They
  resolve under the configured base, giving
  `https://docs.aspose.com/tex/java/latex-to-pdf/`. This avoids the citation bug
  seen in the TeX/.NET acquisition converters.
- Theme markup is resolved before parsing (`docs_extractor.theme_markup`):
  - `{{<section overview>}}` (on all 60 pages) is a layout marker and is dropped,
    so it no longer produces `UNSUPPORTED_HUGO_SHORTCODE`;
  - `{{< emoticons/tick >}}` (8, supported-formats table) becomes `✓`;
  - `{{lang.url-fragment}}` (99, inside root-relative links such as
    `/tex/{{lang.url-fragment}}java/conversion/`) is removed.
- Java code comes only from Gists: 44 distinct files in 5 Gists of
  `aspose-com-gists`. Other fences are `tex` (282), `text` (4) and unlabelled.
- `.run()` counts as Java evidence when relabelling `csharp` highlight blocks
  (Words already used `get/set/save/insert/append/execute`).
- Remaining `{{` in chunk text is genuine LaTeX inside `tex` examples
  (`{{\hat A}}`), not Hugo markup.

### Upstream defects

- `general-articles/latex-ams-math/latex-structures-for-equations` contains 3
  C# blocks (`string equation = @"..."`, `options.Preamble = @"..."`) on a Java
  page. They keep their `csharp` label.
- The developer-guide "API Reference" link points to
  `reference.aspose.com/page/java/` (Aspose.Page). In-body links are not used as
  citations.
- Many docs pages carry `lastmod` dates from 2024; release alignment of the docs
  to a specific SDK version needs a content review.

## Retrieval profile (serving only)

`retrieval-profile.json` 1.0.0 has 11 rules: LaTeX to PDF, PNG, image, XPS and
SVG (TeXJob.run plus the matching device and save options); math, formula and
equation rendering (`MathRendererPlugin`, `PngMathRendererPluginOptions`,
`PngMathRenderer`); figure rendering; LaTeX repair (`LaTeXRepairer`). No
namespaces are excluded. It validates against engine-core's
`RetrievalProfile` model (`com.<product>.` prefix support required).


## Verification (11 November 2026)

Unit tests: 23 pass (`python -m unittest discover -s tests`) on Linux and
Windows (Python 3.13). `scripts/audit_sources.py` with the real Gist cache
(44 of 44 examples available):

| Source | Revision | Pages | Errors | Chunks | Symbols |
| --- | --- | --- | --- | --- | --- |
| docs `en/java` | `75002cc2` | 60 | 0 | 204 | 0 |
| apiref `english/java` | `bbfcba7d` (24.9) | 98 | 0 | 643 | 636 |
