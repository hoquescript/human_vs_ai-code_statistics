import shutil
from pathlib import Path

CODE_DIR = Path("temp")
REPORTS_DIR = Path("reports")


def setup_directories() -> tuple[Path, Path]:
    # return CODE_DIR, REPORTS_DIR

    for directory in (CODE_DIR, REPORTS_DIR):
        shutil.rmtree(directory, ignore_errors=True)
        directory.mkdir(parents=True)

    return CODE_DIR, REPORTS_DIR
