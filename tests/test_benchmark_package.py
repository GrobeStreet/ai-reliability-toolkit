import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ai-reliability-audit"
SCRIPT = SKILL / "scripts/audit_benchmark.py"
DEMO = SKILL / "scripts/reproduce_demo.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = load(SCRIPT, "audit")
builder = load(ROOT / "submission/build_package.py", "builder")


class PairedAuditTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((SKILL / "examples/paired-input.json").read_text())

    def cli(self, raw, script=SCRIPT):
        return subprocess.run([sys.executable, str(script)], input=raw, text=True,
                              capture_output=True)

    def test_supplied_example_and_reference_agree(self):
        result = audit.analyze(self.document)
        expected = json.loads((SKILL / "examples/paired-output.json").read_text())
        expected.pop("execution")
        self.assertEqual(result, expected)
        self.assertEqual(result["changed_item_ids"], ["q1", "q2"])
        self.assertEqual(result["readiness"], "not_assessed")

    def test_order_does_not_change_pairing_or_canonical_hash(self):
        before = audit.analyze(self.document)
        self.document["rows"].reverse()
        self.assertEqual(before, audit.analyze(self.document))

    def test_invalid_or_ambiguous_cells_rejected(self):
        cases = []
        for value in ("false", 0, 1, None):
            doc = copy.deepcopy(self.document)
            doc["rows"][0]["correct"] = value
            cases.append(doc)
        doc = copy.deepcopy(self.document);doc["rows"].pop();cases.append(doc)
        doc = copy.deepcopy(self.document);doc["rows"].append(doc["rows"][0]);cases.append(doc)
        doc = copy.deepcopy(self.document);doc["rows"][0]["item_id"] = " q1";cases.append(doc)
        for doc in cases:
            with self.subTest(doc=doc), self.assertRaises(ValueError):
                audit.analyze(doc)

    def test_empty_and_one_condition_rejected(self):
        for rows in ([], [{"item_id": "q", "condition": "a", "correct": True}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                audit.analyze({"rows": rows})

    def test_invalid_expectations_are_errors(self):
        for value in (True, "0.5", -0.1, 1.1, float("nan"), float("inf")):
            doc = copy.deepcopy(self.document)
            doc["expected_metrics"]["max_drift"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit.analyze(doc)

    def test_mismatch_is_preserved_and_cli_exit_is_one(self):
        self.document["expected_metrics"]["max_drift"] = 0.2
        run = self.cli(json.dumps(self.document))
        self.assertEqual(run.returncode, 1)
        self.assertEqual(json.loads(run.stdout)["reproduction"]["status"], "mismatch")
        self.assertEqual(self.document["expected_metrics"]["max_drift"], 0.2)

    def test_missing_criteria_does_not_create_readiness(self):
        result = audit.analyze(self.document)
        self.assertEqual(result["observed_criteria"]["status"], "not_assessed")
        self.document["criteria"] = {"max_correctness_flip_rate": 0.1}
        self.assertEqual(audit.analyze(self.document)["observed_criteria"]["status"], "not_assessed")

    def test_predeclared_criteria_are_descriptive_not_readiness(self):
        self.document.update(criteria={"max_accuracy_drift": 0.03,
                                       "max_correctness_flip_rate": 0.1}, criteria_predeclared=True)
        result = audit.analyze(self.document)
        self.assertEqual(result["observed_criteria"]["status"], "observed_criterion_failed")
        self.assertEqual(result["readiness"], "not_assessed")
        self.assertTrue(result["observed_criteria"]["checks"]["max_accuracy_drift"]["met"])

    def test_accuracy_drift_at_inclusive_boundary_meets_threshold(self):
        rows = [{"item_id": str(i), "condition": c, "correct": i < count}
                for c, count in [("a", 5), ("b", 8)] for i in range(10)]
        result = audit.analyze({"rows": rows, "criteria": {"max_accuracy_drift": 0.3},
                                "criteria_predeclared": True})
        self.assertEqual(result["metrics"]["max_drift"], 0.3)
        self.assertEqual(result["observed_criteria"]["status"], "observed_criteria_met")

    def test_duplicate_json_keys_and_nonfinite_literals_rejected(self):
        for raw in ('{"rows":[],"rows":[]}', '{"rows":NaN}', '{"rows":Infinity}'):
            with self.subTest(raw=raw):
                run = self.cli(raw)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, "")
                self.assertIn("error", json.loads(run.stderr))

    def test_multiple_conditions_count_changed_item_once(self):
        doc = {"rows": [{"item_id": "q", "condition": c, "correct": v}
                        for c, v in [("a", True), ("b", False), ("c", True)]]}
        result = audit.analyze(doc)
        self.assertEqual(result["counts"]["items_with_correctness_changes"], 1)
        self.assertEqual(result["metrics"]["correctness_flip_rate"], 1)

    def test_scripts_run_unchanged_in_isolated_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            a = directory / "a.py";a.write_bytes(SCRIPT.read_bytes())
            b = directory / "b.py";b.write_bytes(DEMO.read_bytes())
            toy = subprocess.run([sys.executable, "-I", str(b)], cwd=directory,
                                 text=True, capture_output=True, check=True)
            result = subprocess.run([sys.executable, "-I", str(a)], cwd=directory,
                                    input=toy.stdout, text=True, capture_output=True, check=True)
            output = json.loads(result.stdout)
            expected = json.loads((SKILL / "examples/toy-output.json").read_text())
            output.pop("execution");expected.pop("execution")
            self.assertEqual(output, expected)
            self.assertEqual(output["metrics"]["correctness_flip_rate"], 1)
            self.assertEqual(output["reproduction"]["status"], "matches_supplied_expectations")

    def test_package_is_one_skill_and_scripts_stay_small(self):
        package = builder.build(ROOT)
        names = [f["path"] for f in package["files"]]
        self.assertEqual(names.count("SKILL.md"), 1)
        self.assertNotIn("submission/agensi-listing.md", names)
        for file in package["files"]:
            if file["path"].endswith(".py"):
                self.assertLess(len(file["content"].encode()), 20000)


if __name__ == "__main__":
    unittest.main()
