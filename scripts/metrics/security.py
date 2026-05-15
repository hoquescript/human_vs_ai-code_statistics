import subprocess
import sys
from pathlib import Path


def security_analysis(code_dir: Path, reports_dir: Path):
    print(f"Running security analysis in {code_dir}...")
    output = reports_dir / "security.json"

    result = subprocess.run(
        [
            "semgrep",
            "scan",
            "--pro",
            "--config",
            "p/security-audit",
            "--no-git-ignore",
            "--json",
            "--output",
            str(output.resolve()),
            "--verbose",
            "--jobs",
            "4",
            str(code_dir.resolve()),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Semgrep scan failed: {result.stderr}")
        sys.exit(result.returncode)

    print(f"Security analysis completed. Report written to {output}")
