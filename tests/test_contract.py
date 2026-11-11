"""Run with stdlib unittest; no engine installation needed."""

import json
import unittest

from helpers import FIXTURES, MANIFEST, extract_api, request, run_worker

BASE = "https://reference.aspose.com/tex/java"


def by_fqn(symbols, fqn):
    return [s for s in symbols if s["member_fqn"] == fqn]


class JavaTypePageTest(unittest.TestCase):
    def test_type_row_uses_java_identity_and_declaration(self):
        output = extract_api("texjob-real.md", "texjob")
        document = output["normalized_document"]["document"]
        self.assertEqual(document["symbol_fqn"], "com.aspose.tex.TeXJob")
        self.assertEqual(document["symbol_kind"], "class")
        self.assertEqual(document["canonical_url"], BASE + "/com.aspose.tex/texjob/")
        (type_row,) = by_fqn(output["symbols"], "com.aspose.tex.TeXJob")
        self.assertEqual(type_row["kind"], "class")
        self.assertEqual(type_row["parent_fqn"], "com.aspose.tex")
        self.assertEqual(type_row["signature"], "public class TeXJob")
        self.assertEqual(type_row["payload"]["section_anchor"], "#")
        self.assertEqual(type_row["language"], "java")

    def test_constructor_overloads_keep_anchor_signature_and_parent(self):
        output = extract_api("texjob-real.md", "texjob")
        rows = by_fqn(output["symbols"], "com.aspose.tex.TeXJob.TeXJob")
        self.assertEqual(
            sorted(r["signature"] for r in rows),
            [
                "public TeXJob(Device device, TeXOptions options)",
                "public TeXJob(InputStream stream, Device device, TeXOptions options)",
                "public TeXJob(String path, Device device, TeXOptions options)",
            ],
        )
        self.assertIn(
            "#TeXJob-java.lang.String-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-",
            {r["payload"]["section_anchor"] for r in rows},
        )
        for row in rows:
            self.assertEqual(row["kind"], "constructor")
            self.assertEqual(row["parent_fqn"], "com.aspose.tex.TeXJob")
            self.assertEqual(row["canonical_url"], BASE + "/com.aspose.tex/texjob/")
        (run,) = by_fqn(output["symbols"], "com.aspose.tex.TeXJob.run")
        self.assertEqual(run["kind"], "method")
        self.assertEqual(run["signature"], "public TeXJobResult run()")
        self.assertEqual(run["payload"]["section_anchor"], "#run--")
        (create,) = by_fqn(output["symbols"], "com.aspose.tex.TeXJob.createFormat")
        self.assertEqual(
            create["signature"], "public static void createFormat(String path, TeXOptions options)"
        )

    def test_enum_constants_are_fields(self):
        output = extract_api("tiffcompression-real.md", "tiffcompression", "com.aspose.tex.rendering")
        self.assertEqual(output["normalized_document"]["document"]["symbol_kind"], "enum")
        (lzw,) = by_fqn(output["symbols"], "com.aspose.tex.rendering.TiffCompression.CompressionLZW")
        self.assertEqual(lzw["kind"], "field")
        self.assertEqual(lzw["signature"], "public static final TiffCompression CompressionLZW")
        self.assertEqual(lzw["parent_fqn"], "com.aspose.tex.rendering.TiffCompression")

    def test_interface_whose_front_matter_closes_inline(self):
        # Upstream writes `---```` on one line for interface pages.
        output = extract_api("ifilecollector-real.md", "ifilecollector")
        codes = {w["code"] for w in output["normalized_document"]["warnings"]}
        self.assertIn("HUGO_FRONT_MATTER_CLOSE_INLINE_CONTENT", codes)
        self.assertEqual(output["normalized_document"]["document"]["symbol_kind"], "interface")
        (row,) = by_fqn(output["symbols"], "com.aspose.tex.IFileCollector")
        self.assertEqual(row["signature"], "public interface IFileCollector")
        rows = by_fqn(output["symbols"], "com.aspose.tex.IFileCollector.getFileNamesByExtension")
        self.assertEqual(len(rows), 2)

    def test_nested_type_keeps_enclosing_type_in_identity(self):
        # Upstream directory is `float/`; title, declaration and URL say Size2D.Float.
        output = extract_api("size2d-float-real.md", "float")
        document = output["normalized_document"]["document"]
        self.assertEqual(document["symbol_fqn"], "com.aspose.tex.Size2D.Float")
        self.assertEqual(document["canonical_url"], BASE + "/com.aspose.tex/size2d.float/")
        (row,) = by_fqn(output["symbols"], "com.aspose.tex.Size2D.Float")
        self.assertEqual(
            row["signature"], "public static class Size2D.Float extends Size2D implements Serializable"
        )
        constructors = by_fqn(output["symbols"], "com.aspose.tex.Size2D.Float.Float")
        self.assertEqual({r["kind"] for r in constructors}, {"constructor"})
        self.assertEqual(len(constructors), 2)


class JavaChunkTest(unittest.TestCase):
    def test_chunks_cite_their_member_and_never_span_two(self):
        output = extract_api("texjob-real.md", "texjob")
        chunks = output["chunk_records"]
        anchors = [c["section_anchor"] for c in chunks]
        self.assertEqual(anchors[0], "#")
        self.assertIn("#run--", anchors)
        for chunk in chunks:
            self.assertEqual(chunk["symbol_fqn"], "com.aspose.tex.TeXJob")
            self.assertLessEqual(len(chunk["section_path"]), 3)
            if chunk["section_anchor"] == "#run--":
                self.assertTrue(chunk["section_path"][1].startswith("run("))
                self.assertNotIn("createFormat(String", chunk["text"])

    def test_declarations_are_signatures_not_executable_snippets(self):
        output = extract_api("texjob-real.md", "texjob")
        for chunk in output["chunk_records"]:
            for snippet in chunk["executable_snippets"]:
                self.assertFalse(snippet["code"].startswith("public "), snippet["code"])
        self.assertTrue(
            any(c["chunk_type"] == "api_signature" for c in output["chunk_records"])
        )
        self.assertTrue(any("| Method | Description |" in c["text"]
                            for c in output["chunk_records"]))


class ScopeAndUrlTest(unittest.TestCase):
    def test_package_and_root_pages_are_namespaces_without_symbols(self):
        for relative, raw in (
            ("english/java/_index.md", "---\ntitle: Aspose.TeX for Java\nurl: /java/\n---\n"
             "## Packages\n| Package | Description |\n| --- | --- |\n"),
            ("english/java/com.aspose.tex.rendering/_index.md",
             "---\ntitle: com.aspose.tex.rendering\nurl: /java/com.aspose.tex.rendering/\n---\n"
             "## Classes\n"),
        ):
            with self.subTest(relative=relative):
                result = run_worker(request("apiref", raw, relative))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                output = json.loads(result.stdout)["result"]
                self.assertEqual(output["symbols"], [])
                self.assertIsNone(output["normalized_document"]["document"]["symbol_fqn"])

    def test_other_platforms_and_products_are_rejected(self):
        relative = "english/java/com.aspose.tex/texjob/_index.md"
        raw = (FIXTURES / "texjob-real.md").read_text(encoding="utf-8")
        for override in ({"product_id": "aspose.words"}, {"language": "net"},
                         {"plugin_id": "aspose.tex.net"}):
            with self.subTest(override=override):
                result = run_worker(request("apiref", raw, relative, **override))
                self.assertNotEqual(result.returncode, 0)
        net_layout = "english/net/aspose.tex/texjob/_index.md"
        result = run_worker(request("apiref", raw, net_layout))
        self.assertNotEqual(result.returncode, 0)

    def test_canonical_urls(self):
        for kind in ("docs", "apiref"):
            source = MANIFEST["sources"][kind]
            base = source["canonical_base_url"]
            origin = base.removesuffix("/tex/java")
            cases = [
                ("_index.md", None, base + "/"),
                ("_index.md", "/java/", base + "/"),
                ("_index.md", "/java", base + "/"),
                ("guide/_index.md", "/java/guide/", base + "/guide/"),
                ("guide/_index.md", "/java/guide/?view=x#example", base + "/guide/?view=x#example"),
                ("guide/_index.md", "/javascript/guide/", origin + "/javascript/guide/"),
                ("guide/details.md", None, base + "/guide/details/"),
                ("guide/_index.md", "/tex/java/guide/", base + "/guide/"),
                ("guide/_index.md", "guide/#example", base + "/guide/#example"),
                ("guide/_index.md", "https://example.com/x/", "https://example.com/x/"),
                ("guide/_index.md", "//example.com/guide/", None),
                ("guide/_index.md", "javascript:alert(1)", None),
            ]
            for path, override, expected in cases:
                with self.subTest(kind=kind, path=path, override=override):
                    relative = source["prefix"] + "/" + path
                    frontmatter = "title: Guide\n"
                    if override is not None:
                        frontmatter += "url: " + json.dumps(override) + "\n"
                    raw = "---\n" + frontmatter + "---\n# Guide\nUseful content.\n"
                    result = run_worker(request(kind, raw, relative))
                    if expected is None:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn("Canonical URL overrides", result.stdout)
                        continue
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    response = json.loads(result.stdout)["result"]
                    self.assertEqual(
                        response["normalized_document"]["document"]["canonical_url"], expected
                    )
                    for chunk in response["chunk_records"]:
                        self.assertEqual(chunk["canonical_url"], expected)

    def test_minimal_docs_fixture_used_by_deployment_check(self):
        raw = (FIXTURES / "docs.md").read_text(encoding="utf-8")
        result = run_worker(request("docs", raw, MANIFEST["sources"]["docs"]["prefix"] + "/_index.md"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)["result"]
        self.assertEqual(
            output["normalized_document"]["document"]["canonical_url"],
            "https://docs.aspose.com/tex/java/guide/",
        )
        self.assertEqual([b["language"] for b in output["page"]["code_blocks"]], ["java"])
        self.assertTrue(output["chunk_records"])


if __name__ == "__main__":
    unittest.main()
