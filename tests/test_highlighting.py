import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path


REMARK_JS = Path(__file__).parents[1] / "src" / "podium" / "resources" / "remark.js"


@unittest.skipUnless(
    shutil.which("node"),
    "node is required to exercise bundled remark.js",
)
class HighlightingTests(unittest.TestCase):
    def test_toml_blocks_are_not_autodetected_as_sql(self):
        script = textwrap.dedent(
            """
            const fs = require("fs");
            global.window = {};
            global.document = {
              createElement() {
                return {type: "", innerHTML: "", firstChild: null};
              },
              getElementsByTagName() {
                return [{firstChild: null, insertBefore() {}}];
              }
            };

            eval(fs.readFileSync(process.argv[1], "utf8"));

            const block = {
              className: "toml",
              parentNode: {className: ""},
              childNodes: [{
                nodeType: 3,
                nodeValue:
                  "[[packages.wheels]]\\n" +
                  "name = \\"demo\\"\\n" +
                  "upload-time = 1\\n" +
                  "size = 2\\n"
              }],
            };

            window.remark.highlighter.engine.highlightBlock(block, "  ");

            if (block.className !== "toml") {
              throw new Error(`Unexpected class name: ${block.className}`);
            }
            if ((block.innerHTML || "").includes("sql")) {
              throw new Error(`TOML was highlighted as SQL: ${block.innerHTML}`);
            }
            """
        )

        result = subprocess.run(
            ["node", "-e", script, str(REMARK_JS)],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
