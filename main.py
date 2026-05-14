from scripts.utils.get_data import get_data
from scripts.utils.create_file import create_file_from_commit


def main():
    # Get data
    df = get_data()
    print(df.columns)
    print(df.shape)
    print(df["language"].value_counts())
    print(df.describe())

    # Create files
    # create_file_from_commit(df)


if __name__ == "__main__":
    main()
