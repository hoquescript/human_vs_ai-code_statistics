from scripts.utils.get_data import get_data
from scripts.utils.create_file import create_file_from_commit
from scripts.utils.setup import setup_directories
from scripts.metrics.security import security_analysis
from scripts.metrics.complexity import complexity_analysis


def main():
    # Setup directories
    CODE_DIR, REPORTS_DIR = setup_directories()

    # Get data
    df = get_data(sample=True)

    # Create files
    files_created = create_file_from_commit(df, CODE_DIR)
    if files_created != df.shape[0]:
        raise ValueError(f"Files created: {files_created} != {df.shape[0]}")

    # Run security analysis
    security_analysis(code_dir=CODE_DIR, reports_dir=REPORTS_DIR)

    # Run complexity analysis
    complexity_analysis(code_dir=CODE_DIR, reports_dir=REPORTS_DIR)


if __name__ == "__main__":
    main()
