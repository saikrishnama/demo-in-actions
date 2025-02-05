#!/usr/bin/env python3
import subprocess

def get_diff(mr_ref, main_branch="main"):
    """
    Get the diff output (as a string) between the main branch and the merge request branch.
    This command compares what changes exist in the merge request branch that are not in main.
    """
    try:
        # The diff command returns the changes that are in mr_ref but not in main_branch.
        result = subprocess.run(
            ["git", "diff", f"{main_branch}..{mr_ref}"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error comparing {mr_ref} with {main_branch}: {e}")
        return None

def main():
    # List of merge request branch names.
    merge_requests = [
        "mr/1",
        "mr/2",
        "mr/3",
        # Add more merge request branches as needed.
    ]

    # Open the output files.
    with open("present.txt", "w") as present_file, open("not_present.txt", "w") as not_present_file:
        for mr in merge_requests:
            diff_output = get_diff(mr)
            if diff_output is None:
                # An error occurred. You might want to log or handle this case differently.
                not_present_file.write(f"{mr} (error comparing branches)\n")
                continue

            if diff_output == "":
                # No differences found between mr and main branch.
                present_file.write(f"Merge request {mr} changes are already present in main branch.\n")
                print(f"[PRESENT] {mr} - No diff found against main.")
            else:
                # Differences exist, so the merge request changes are not (completely) in main.
                not_present_file.write(f"{mr}\n")
                print(f"[NOT PRESENT] {mr} - Diff detected.")

if __name__ == "__main__":
    main()
