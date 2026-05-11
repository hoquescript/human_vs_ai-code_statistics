import subprocess

INPUT = "temp/"
OUTPUT = "data/report/security.json"
LANGUAGES = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#']

def analyze():
    return subprocess.run([
        "semgrep",
        "scan",
        "--pro",
        "--config", "p/security-audit",
        "--json", "--output", OUTPUT,
        "--verbose",
        "--jobs", "4",
        INPUT
    ], capture_output=True, text=True)


if __name__ == "__main__":
    result = analyze()
    if(result.returncode != 0):
        print(f"Semgrep scan failed: {result.stderr}")
    else:
        print("Success")

