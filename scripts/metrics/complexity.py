import csv
import shutil
import subprocess
import sys
from pathlib import Path

UNDERSTAND_EXE = Path("/Applications/Understand.app/Contents/MacOS/und")
UNDERSTAND_PYTHON = Path("/Applications/Understand.app/Contents/MacOS/Python")
UNDERSTAND_PROJECT = Path(".analysis.und")
LANGUAGES = ["Python", "Java", "Web", "c++", "c#"]

METRICS = [
    # --- Size Metrics (Volume & Density) ---
    "CountLine",  # Total lines
    "CountLineCode",  # Code lines
    "CountLineComment",  # Comment lines
    "CountLineBlank",  # Blank lines
    "CountStmt",  # Total statements
    "CountStmtDecl",  # Declarative statements
    "CountStmtExe",  # Executable statements
    "CountLineCodeDecl",  # Lines of code with declarations
    "CountLineCodeExe",  # Lines of code with execution
    # --- Average Size Metrics (Consistency) ---
    "AvgLine",
    "AvgLineCode",
    "AvgLineComment",
    "AvgLineBlank",
    # --- Declaration Metrics (Structure Count) ---
    "CountDeclClass",  # Number of classes
    "CountDeclFunction",  # Number of functions
    "CountDeclExecutableUnit",  # Number of executable units
    # --- Complexity Metrics (Control Flow) ---
    "Cyclomatic",  # Cyclomatic complexity
    "MaxCyclomatic",  # Max complexity in file
    "AvgCyclomatic",  # Average complexity
    "SumCyclomatic",  # Total complexity
    "MaxNesting",  # Deepest nesting level
    # --- Documentation Metrics (Readability) ---
    "RatioCommentToCode",  # Ratio of comments to code
    # --- Halstead Metrics (Lexical Entropy/Vocabulary) ---
    "HalsteadEffort",  # Halstead Effort
    "HalsteadDifficulty",  # Halstead Difficulty
    # --- Architecture/OO Metrics (Coupling & Inheritance) ---
    "CountClassCoupled",  # Coupling (Dependencies)
    "MaxInheritanceTree",  # Inheritance Depth
]


def get_halstead_volume(report: dict) -> float:
    try:
        effort = float(str(report.get("HalsteadEffort", "0")).replace(",", ""))
        difficulty = float(str(report.get("HalsteadDifficulty", "0")).replace(",", ""))
        return effort / difficulty if difficulty != 0 else 0.0
    except ValueError:
        return 0.0


def parse_metrics(project_path: Path, output_path: Path, code_dir: Path):
    if str(UNDERSTAND_PYTHON) not in sys.path:
        sys.path.append(str(UNDERSTAND_PYTHON))
    import understand

    db = understand.open(str(project_path))
    code_dir_resolved = code_dir.resolve()

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "HalsteadVolume", *METRICS])
        writer.writeheader()

        for entity in db.ents("File"):
            if entity.library():
                continue
            if not Path(entity.longname()).is_relative_to(code_dir_resolved):
                continue

            report = entity.metric(METRICS)

            max_dit = 0
            max_cbo = 0
            for ref in entity.refs("Define", "Class"):
                class_metrics = ref.ent().metric(
                    ["MaxInheritanceTree", "CountClassCoupled"]
                )
                dit = class_metrics.get("MaxInheritanceTree") or 0
                cbo = class_metrics.get("CountClassCoupled") or 0
                if dit > max_dit:
                    max_dit = dit
                if cbo > max_cbo:
                    max_cbo = cbo

            report["MaxInheritanceTree"] = max_dit
            report["CountClassCoupled"] = max_cbo
            report["HalsteadVolume"] = get_halstead_volume(report)
            report["Name"] = entity.longname()

            writer.writerow(report)

    db.close()


def complexity_analysis(code_dir: Path, reports_dir: Path):
    print(f"Running complexity analysis in {code_dir}...")
    output = reports_dir / "complexity.csv"

    shutil.rmtree(UNDERSTAND_PROJECT, ignore_errors=True)

    # Create project
    subprocess.run(
        [
            str(UNDERSTAND_EXE),
            "create",
            "-languages",
            *LANGUAGES,
            str(UNDERSTAND_PROJECT),
        ],
        check=True,
    )
    # Add codes from code_dir to project
    subprocess.run(
        [str(UNDERSTAND_EXE), "add", str(code_dir.resolve()), str(UNDERSTAND_PROJECT)],
        check=True,
    )
    # Analyze project
    subprocess.run(
        [str(UNDERSTAND_EXE), "analyze", str(UNDERSTAND_PROJECT)],
        capture_output=True,
        check=True,
    )

    parse_metrics(UNDERSTAND_PROJECT, output, code_dir)
    print(f"Complexity analysis completed. Report written to {output}")
    print("_" * 80)
