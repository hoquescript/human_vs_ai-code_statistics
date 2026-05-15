from datasets import load_dataset, concatenate_datasets
import uuid


def get_data(sample=True):
    dataset = load_dataset("HanxiGuo/CodeMirage")
    dataset = concatenate_datasets([dataset["train"], dataset["test"]])

    df = dataset.to_pandas()

    # Extract language: Python, Java, JavaScript, CPP, CSHARP from the code column
    df = df[df["language"].isin(["Python", "Java", "JavaScript", "CPP", "CSharp"])]

    # Add a unique id to the dataframe
    df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    # Drop rows where the code column is null
    df = df.dropna(subset=["code"])

    if sample:
        df = df.sample(n=10)

    print(f"Columns: {df.columns}")
    print(f"Shape: {df.shape}")
    print(f"Language: {df['language'].value_counts()}")
    print(f"Describe: {df.describe()}")

    return df
