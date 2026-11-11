"""Offline tests for Java documentation: Gist examples, highlight labels, cleanup."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from adcs_tex_java import docs_extractor, gist_examples, worker  # noqa: E402
from helpers import FIXTURES, request  # noqa: E402

OWNER = "aspose-com-gists"
GIST_ID = "a30f406f6b8ace1b7d15c68a1df75c6d"
SENDER = "Example-ConvertLaTeXToPDF-Alternative.java"
HELLO = "Example-ConvertLaTeXToPDF-Simplest.java"
SHORTCODE = '{{< gist "' + OWNER + '" "' + GIST_ID + '" "' + HELLO + '" >}}'
CODE = (
    "TeXOptions options = TeXOptions.consoleAppOptions(TeXConfig.objectLaTeX());\n"
    "options.setOutputWorkingDirectory(new OutputFileSystemDirectory(outputDir));\n"
    "options.setSaveOptions(new PdfSaveOptions());\n"
    'new TeXJob("hello-world.ltx", new PdfDevice(), options).run();'
)


def entry(code):
    return {"revision": "a" * 40, "code": code,
            "sha256": hashlib.sha256(code.encode()).hexdigest()}


class GistExamplesTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.cache = self.root / "examples.json"
        sender = (
            "PdfDevice device = new PdfDevice();\n"
            'new TeXJob("hello-world.ltx", device, options).run();'
        )
        self.cache.write_text(json.dumps({"schema": 1, "examples": {
            f"{OWNER}/{GIST_ID}/{HELLO}": entry(CODE),
            f"{OWNER}/{GIST_ID}/{SENDER}": entry(sender),
        }}))
        patcher = patch.object(docs_extractor, "expand", side_effect=lambda t: (
            gist_examples.expand(t, cache_path=self.cache)
        ))
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_docs(self, raw, relative="en/java/developer-guide/conversion/latex-to-pdf/_index.md"):
        return worker.handle(request("docs", raw, relative))

    def test_real_page_gists_become_java_and_console_output_keeps_its_label(self):
        page = (FIXTURES / "latex-to-pdf-docs-real.md").read_text(encoding="utf-8")
        result = self.run_docs(page)
        document = result["normalized_document"]["document"]
        self.assertEqual(
            document["canonical_url"], "https://docs.aspose.com/tex/java/latex-to-pdf/"
        )
        languages = [b["language"] for b in result["page"]["code_blocks"]]
        self.assertEqual(sorted(languages), ["java", "java", "text"])
        snippets = [s for c in result["chunk_records"] for s in c["executable_snippets"]]
        self.assertIn(CODE, [s["code"] for s in snippets])
        text = "\n".join(c["text"] for c in result["chunk_records"])
        for artifact in ("{{<", "{{%", "gist", "url-fragment"):
            self.assertNotIn(artifact, text)

    def test_tex_theme_shortcodes_are_resolved_without_warnings(self):
        page = (FIXTURES / "supported-file-formats-docs-real.md").read_text(encoding="utf-8")
        result = self.run_docs(page, "en/java/getting-started/supported-file-formats/_index.md")
        self.assertFalse(result["page"]["parse_warnings"])
        text = "\n".join(c["text"] for c in result["chunk_records"])
        self.assertIn("\u2713", text)
        self.assertNotIn("emoticons", text)
        raw = (
            "---\ntitle: Guide\nurl: /java/guide/\n---\n{{<section overview>}}\n\n"
            "## Overview\n\nSee [Conversion](/tex/{{lang.url-fragment}}java/conversion/).\n"
        )
        result = self.run_docs(raw, "en/java/guide/_index.md")
        self.assertFalse(result["page"]["parse_warnings"])
        text = "\n".join(c["text"] for c in result["chunk_records"])
        self.assertIn("(/tex/java/conversion/)", text)
        self.assertNotIn("section", text)

    def test_csharp_label_is_corrected_only_for_evident_java(self):
        cases = (
            ('Document doc = new Document();\ndoc.save("out.pdf");', "java"),
            ('String[] names = {"A"};', "java"),
            ('var doc = new Document();\ndoc.Save("out.pdf");', "csharp"),
            ("public Shape InsertOleObject(Stream stream, string progId)", "csharp"),
            ('<<[s.getName()]>> says: "<<[s.getMessage()]>>."', "csharp"),
            ("persons.count()", "csharp"),
        )
        for code, expected in cases:
            with self.subTest(code=code):
                raw = "# Example\n{{< highlight csharp >}}\n" + code + "\n{{< /highlight >}}\n"
                result = self.run_docs(raw, "en/java/example/_index.md")
                self.assertEqual(result["page"]["code_blocks"][0]["language"], expected)

    def test_html_headings_and_alerts_are_removed_from_text(self):
        raw = """---
title: Convert a Document
url: /java/convert-a-document/
---
<h2>Convert Word to PDF</h2>
{{% alert color="primary" %}}
Use the <strong>save</strong> method.
{{% /alert %}}
```java
builder.insertHtml("<h2>Heading inside code</h2>");
```
"""
        result = self.run_docs(raw, "en/java/convert-a-document/_index.md")
        text = result["page"]["body_plain"]
        self.assertIn("Convert Word to PDF", text)
        self.assertNotIn("<h2>Convert", text)
        self.assertNotIn("<strong>", text)
        self.assertIn("<h2>Heading inside code</h2>", result["page"]["code_blocks"][0]["code"])

    def test_missing_and_corrupt_cache_fail_explicitly(self):
        with self.assertRaisesRegex(ValueError, "Missing Gist"):
            gist_examples.expand(SHORTCODE, cache_path=self.root / "missing.json")
        data = json.loads(self.cache.read_text(encoding="utf-8"))
        next(iter(data["examples"].values()))["code"] = "changed"
        self.cache.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "checksum"):
            gist_examples.expand(SHORTCODE, cache_path=self.cache)

    def test_prepare_reuses_pinned_cache_without_network(self):
        (self.root / "page.md").write_text(SHORTCODE, encoding="utf-8")
        with patch.object(gist_examples.subprocess, "run") as run:
            result = gist_examples.prepare(self.root, self.cache)
        run.assert_not_called()
        self.assertEqual(result["downloaded"], 0)

    def test_prepare_records_revision_and_reuses_duplicate_reference(self):
        (self.root / "page.md").write_text(SHORTCODE + "\n" + SHORTCODE, encoding="utf-8")
        with patch.object(gist_examples.subprocess, "run") as run, patch.object(
            gist_examples.subprocess, "check_output", side_effect=[
                "b" * 40 + "\n", f"100644 blob {'c' * 40}\t{HELLO}\0".encode(), CODE.encode(),
            ]
        ):
            result = gist_examples.prepare(self.root, self.cache, refresh=True)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(result["references"], 1)
        examples = json.loads(self.cache.read_text(encoding="utf-8"))["examples"]
        cached = examples[f"{OWNER}/{GIST_ID}/{HELLO}"]
        self.assertEqual(cached["revision"], "b" * 40)
        self.assertEqual(gist_examples.checked_code(cached), CODE)

    def test_failed_download_preserves_previous_cache(self):
        original = self.cache.read_bytes()
        (self.root / "page.md").write_text(SHORTCODE, encoding="utf-8")
        with patch.object(gist_examples.subprocess, "run", side_effect=RuntimeError("offline")):
            with self.assertRaisesRegex(RuntimeError, "offline"):
                gist_examples.prepare(self.root, self.cache, refresh=True)
        self.assertEqual(self.cache.read_bytes(), original)

    def test_files_missing_upstream_are_recorded_and_pages_still_extract(self):
        (self.root / "page.md").write_text(SHORTCODE, encoding="utf-8")
        with patch.object(gist_examples.subprocess, "run"), patch.object(
            gist_examples.subprocess, "check_output", side_effect=[
                "b" * 40 + "\n", f"100644 blob {'c' * 40}\tOther.java\0".encode(),
            ]
        ):
            report = gist_examples.prepare(self.root, self.cache, refresh=True)
        self.assertEqual(report["unavailable"], [f"{OWNER}/{GIST_ID}/{HELLO}"])
        self.assertEqual(report["downloaded"], 0)
        examples = json.loads(self.cache.read_text(encoding="utf-8"))["examples"]
        entry = examples[f"{OWNER}/{GIST_ID}/{HELLO}"]
        self.assertTrue(entry["unavailable"])
        self.assertEqual(entry["revision"], "b" * 40)
        # Reuse without network keeps the recorded fact.
        with patch.object(gist_examples.subprocess, "run") as run:
            self.assertEqual(gist_examples.prepare(self.root, self.cache)["unavailable"],
                             report["unavailable"])
        run.assert_not_called()
        result = self.run_docs(
            "# Mail merge\n\nInsert images.\n\n" + SHORTCODE + "\n\nMore prose.\n"
        )
        warnings = result["normalized_document"]["warnings"]
        self.assertEqual([w["code"] for w in warnings], ["GIST_EXAMPLE_UNAVAILABLE"])
        self.assertIn(HELLO, warnings[0]["message"])
        self.assertFalse(result["page"]["code_blocks"])
        text = "\n".join(c["text"] for c in result["chunk_records"])
        self.assertIn("More prose.", text)
        self.assertNotIn("adcs:gist-unavailable", text)

    def test_cache_round_trips_characters_outside_the_windows_code_page(self):
        code = 'String s = "\ufffd \u2192 \u4e2d";'
        (self.root / "page.md").write_text(SHORTCODE, encoding="utf-8")
        with patch.object(gist_examples.subprocess, "run"), patch.object(
            gist_examples.subprocess, "check_output", side_effect=[
                "b" * 40 + "\n", f"100644 blob {'c' * 40}\t{HELLO}\0".encode(),
                code.encode("utf-8"),
            ]
        ):
            gist_examples.prepare(self.root, self.cache, refresh=True)
        self.assertIn(code, gist_examples.expand(SHORTCODE, cache_path=self.cache))

    def test_tampered_unavailable_entry_fails(self):
        data = json.loads(self.cache.read_text(encoding="utf-8"))
        data["examples"][f"{OWNER}/{GIST_ID}/{HELLO}"] = {"unavailable": True, "revision": "x"}
        self.cache.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unavailable-entry"):
            gist_examples.expand(SHORTCODE, cache_path=self.cache)

    def test_rejects_ambiguous_reference(self):
        with self.assertRaises(ValueError):
            list(gist_examples.references('{{< gist "owner" "abcd" >}}'))


if __name__ == "__main__":
    unittest.main()
