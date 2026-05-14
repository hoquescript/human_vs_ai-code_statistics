import os
import pandas as pd
import shutil

"""
Create code files from dataframe.

Args:
    commits: DataFrame containing filtered commit files
    language: Programming language name for directory structure
"""


def create_file_from_commit(df: pd.DataFrame):
    print(f"Files to create: {df.shape[0]}")
    shutil.rmtree("temp", ignore_errors=True)
    os.makedirs("temp", exist_ok=True)

    files_created = 0
    for row in df.itertuples(index=False):
        language = row.language
        code = row.code
        filename = row.id + get_extension(language)

        directory = f"temp/{language}"
        os.makedirs(directory, exist_ok=True)

        with open(os.path.join(directory, filename), "w") as f:
            f.write(code)
        files_created += 1

    print(f"Files created: {files_created}")


def get_extension(language: str):
    if language == "Python":
        return ".py"
    elif language == "Java":
        return ".java"
    elif language == "JavaScript":
        return ".js"
    elif language == "CPP":
        return ".cpp"
    elif language == "CSharp":
        return ".cs"
    raise ValueError(f"Unsupported language: {language}")
