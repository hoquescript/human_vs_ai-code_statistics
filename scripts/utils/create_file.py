import re
from pathlib import Path

_CODE_FENCE = re.compile(r"^```\w*\s*$")

_EXTENSIONS = {
    "Python": ".py",
    "Java": ".java",
    "JavaScript": ".js",
    "CPP": ".cpp",
    "CSharp": ".cs",
}


def create_file_from_commit(df, code_dir: Path) -> int:
    print(f"Files to create: {df.shape[0]}")

    files_created = 0
    for row in df.itertuples(index=False):
        language = row.language
        directory = code_dir / language
        directory.mkdir(parents=True, exist_ok=True)

        filename = row.id + get_extension(language)
        (directory / filename).write_text(strip_code_fences(row.code))
        files_created += 1

    print(f"Files created: {files_created}")
    return files_created


def strip_code_fences(code: str) -> str:
    lines = code.splitlines()
    if lines and _CODE_FENCE.match(lines[0]):
        lines = lines[1:]
    if lines and _CODE_FENCE.match(lines[-1]):
        lines = lines[:-1]
    return "\n".join(lines)


def get_extension(language: str) -> str:
    if language not in _EXTENSIONS:
        raise ValueError(f"Unsupported language: {language}")
    return _EXTENSIONS[language]
