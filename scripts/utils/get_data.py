from datasets import load_dataset, concatenate_datasets


def get_data():
    dataset = load_dataset("HanxiGuo/CodeMirage")
    dataset = concatenate_datasets([dataset["train"], dataset["test"]])

    # Extract language: Python, Java, JavaScript, Cpp, Csharp from the code column
    df = dataset.to_pandas()
    df = df[df["language"].isin(["Python", "Java", "JavaScript", "CPP", "CSharp"])]
    return df
