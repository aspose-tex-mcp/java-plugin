# Aspose.TeX for Java extraction plugin

Documentation and API reference extraction for Aspose.TeX for Java, implementing the `adcs.extraction.v1` worker contract. The plugin normalizes Markdown, extracts Java examples and API symbols, produces chunks, and supplies a declarative retrieval profile for the [Aspose Context Engine](https://github.com/aspose-core-mcp/context-engine).

Extraction uses the Python standard library and has no engine or other-plugin runtime dependency. Product identity is `aspose.tex`; API identities are Java packages such as ``com.aspose.tex.TeXJob.run``.

## Project family

These repositories provide documentation-backed MCP services for Aspose.TeX for Java. The shared engine is maintained under **aspose-core-mcp**; the TeX/Java components are maintained under **aspose-tex-mcp**.

| Repository | Responsibility |
| --- | --- |
| [context-engine](https://github.com/aspose-core-mcp/context-engine) | Shared documentation ingestion, indexing, retrieval, and MCP infrastructure |
| [java-plugin](https://github.com/aspose-tex-mcp/java-plugin) **(this repository)** | Aspose.TeX for Java documentation/API extraction and retrieval profile |
| [java-server](https://github.com/aspose-tex-mcp/java-server) | Deployment helpers that combine pinned engine and plugin versions |

Use the [TeX/Java server setup guide](https://github.com/aspose-tex-mcp/java-server/blob/main/docs/setup.md) to deploy the engine with this plugin registered, then follow [client setup](https://github.com/aspose-tex-mcp/java-server/blob/main/docs/clients.md).

## Quick start

Requires Python 3.12 or newer. From this repository root:

```sh
python3.12 -m venv .venv
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -I worker.py < examples/extract-request.json
```

The example runs offline against inline Markdown and prints one JSON response with a normalized document, chunks, and Java API symbols. See the [worker contract](docs/worker-contract.md) for discovery and extraction requests.

Use a source checkout for deployment: the manifest, retrieval profile, and prepared Gist cache are not included in the Python wheel. An installed package exposes `adcs-tex-java-extract` and `python -I -m adcs_tex_java.worker`.

## Prepare and ingest content

1. Follow [source preparation](docs/source-preparation.md) to clone the documentation and API repositories and prepare referenced Gist examples.
2. Register the plugin with the engine using the [integration guide](docs/engine-integration.md).
3. Validate extraction, configure runtime stores, and publish indexed content explicitly.

The plugin does not launch an MCP server or publish data on its own. Source configuration is authoritative in `plugin.json`; citations use `docs.aspose.com/tex/java` and `reference.aspose.com/tex/java`.

## Java specifics

- One API page per type: one type row plus one row per member overload with its own anchor and signature. Chunks carry the member anchor and never span two members.
- Nested types keep the enclosing type: the upstream directory `com.aspose.tex/float/` documents `com.aspose.tex.Size2D.Float`, cited as `/size2d.float/`.
- Interface pages that close front matter inline (`---````) are recovered with a `HUGO_FRONT_MATTER_CLOSE_INLINE_CONTENT` warning.
- TeX documentation theme markup is resolved: `{{<section ...>}}` is dropped, `{{< emoticons/tick >}}` becomes ✓, and `{{lang.url-fragment}}` is removed from links.
- The Java API reference is labelled 24.9; according to the Aspose.TeX team the public API has not changed since, so it matches the current release.
- The retrieval profile maps LaTeX to PDF/PNG/image/XPS/SVG, math and figure rendering, and LaTeX repair questions to the corresponding `com.aspose.tex` types.

See [extraction notes](docs/extraction-notes.md) for details and handled upstream defects.

## Validation

GitHub Actions runs the offline regression suite and extraction example on Python 3.12 and 3.13. See [CONTRIBUTING.md](CONTRIBUTING.md) for local checks.

The [source audit](docs/source-audit.json) records extraction of 60 documentation pages (204 chunks, all 44 Gist examples available) and 98 API pages (643 chunks, 636 symbols) with no errors at the revisions recorded there. It does not establish deployed retrieval quality. Rerun the audit against prepared sources as described in the source preparation guide.

## License and provenance

[MIT License](LICENSE). Derived from the Words/Java extraction plugin (originally the MIT-licensed ADCS pilot), with the original copyright notice preserved. Fixture origins and revisions are documented in [tests/fixtures/README.md](tests/fixtures/README.md).
