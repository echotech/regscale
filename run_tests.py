import os
import subprocess
import sys

def install_dependencies():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Ensure specific versions are installed
    subprocess.check_call([sys.executable, "-m", "pip", "install", "urllib3==1.26.15", "charset-normalizer==2.0.12"])
    
    print("All required packages have been installed.")

def run_tests():
    print("Running tests...")
    browser = input("Enter the browser to use (chrome/firefox/edge) [default: chrome]: ").lower() or "chrome"
    pytest_command = f"pytest -v test_scrape_regscale.py --browser={browser}"
    subprocess.call(pytest_command, shell=True)

if __name__ == "__main__":
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    install_dependencies()
    run_tests()