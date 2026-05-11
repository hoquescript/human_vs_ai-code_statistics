from datasets import load_dataset, concatenate_datasets
import uuid


def get_data():
    dataset = load_dataset("HanxiGuo/CodeMirage")
    dataset = concatenate_datasets([dataset["train"], dataset["test"]])

    df = dataset.to_pandas()

    # Extract language: Python, Java, JavaScript, CPP, CSHARP from the code column
    df = df[df["language"].isin(["Python", "Java", "JavaScript", "CPP", "CSharp"])]

    # Add a unique id to the dataframe
    df["id"] = uuid.uuid4()

    return df
