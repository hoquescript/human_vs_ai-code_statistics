import pandas as pd
from pathlib import Path

_EXTENSIONS = {
    "Python": ".py",
    "Java": ".java",
    "JavaScript": ".js",
    "CPP": ".cpp",
    "CSharp": ".cs",
}


def create_file_from_commit(df: pd.DataFrame, code_dir: Path) -> int:
    print(f"Files to create: {df.shape[0]}")

    files_created = 0
    for row in df.itertuples(index=False):
        directory = code_dir / row.language
        directory.mkdir(parents=True, exist_ok=True)

        filename = row.id + get_extension(row.language)
        (directory / filename).write_text(row.code)
        files_created += 1

    print(f"Files created: {files_created}")
    return files_created


def get_extension(language: str) -> str:
    if language not in _EXTENSIONS:
        raise ValueError(f"Unsupported language: {language}")
    return _EXTENSIONS[language]
