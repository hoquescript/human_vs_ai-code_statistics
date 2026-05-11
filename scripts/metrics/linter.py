import subprocess

def javalint():
    print("Analyzing java files")
    
    input_folder = "temp/java"
    output =  subprocess.run([
        "pmd", 
        "check", 
        "-d", input_folder,
        "-R", "category/java/bestpractices.xml,category/java/codestyle.xml,category/java/errorprone.xml,category/java/design.xml",
        "-f", "csv",
        "--no-cache"
    ], capture_output=True, text=True)

    return output


def cpplint():
    print("Analyzing C++ files")
    
    input_folder = "temp/c++"
    output =  subprocess.run([
        "cppcheck",
        input_folder, 
        "--enable=style,warning,performance,portability", 
        "--inconclusive",    # Catching potential issues even if not 100% sure
        "--xml", 
        "--xml-version=2"
    ], capture_output=True, text=True)

    return output

def pythonlint():
    print("Pythonlint")


if __name__ == "__main__":
    java_report = javalint()
    print(java_report)