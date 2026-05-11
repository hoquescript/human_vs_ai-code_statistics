import os
import pandas as pd
from pathlib import Path

"""
Create code files from dataframe.

Args:
    commits: DataFrame containing filtered commit files
    language: Programming language name for directory structure
"""


def create_file_from_commit(df: pd.DataFrame):
    for index, row in df.itertuples(index=False):
        language = row.language
        code = row.code
        filename = row.id + get_extension(language)

        directory = f"temp/{language}/files"
        os.makedirs(directory, exist_ok=True)

        with open(filename, "w") as f:
            f.write(code)


def get_extension(language: str):
    if language == "Python":
        return ".py"
    elif language == "Java":
        return ".java"
    elif language == "JavaScript":
        return ".js"
    elif language == "C++":
        return ".cpp"
    elif language == "C#":
        return ".cs"
