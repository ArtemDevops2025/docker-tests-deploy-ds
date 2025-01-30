import os

def summarize_tests():
    log_file = "/app/logs/api_test.log"
    if not os.path.exists(log_file):
        print("No logs found. Tests may not have run.")
        return

    print("=== Analyzing Test Results ===")
    all_tests_passed = True

    with open(log_file, "r") as file:
        log_content = file.read()

        if "==> FAILURE" in log_content:
            all_tests_passed = False

    if all_tests_passed:
        print("\n=== Final Summary ===")
        print("Congratulations, all tests were successful.")
    else:
        print("\n=== Final Summary ===")
        print("Error: Some tests failed. Check the logs for details.")

if __name__ == "__main__":
    summarize_tests()