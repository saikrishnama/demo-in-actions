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


###########
#!/usr/bin/env python3
import subprocess
import difflib

def get_diff(mr_ref, main_branch="main"):
    """
    Get the diff output (as a string) between the main branch and the merge request branch.
    This command compares what changes exist in the merge request branch that are not in main.
    """
    try:
        # Fetch the latest changes for both branches
        subprocess.run(["git", "fetch", "origin", main_branch, mr_ref], check=True)

        # Get the list of files changed between the branches
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{main_branch}..{mr_ref}"],
            check=True,
            capture_output=True,
            text=True,
        )
        changed_files = result.stdout.strip().split('\n')
        return changed_files
    except subprocess.CalledProcessError as e:
        print(f"Error comparing {mr_ref} with {main_branch}: {e}")
        return None

def compare_files(file_path, branch1, branch2):
    """
    Compare the content of a file between two branches and return the unified diff.
    """
    try:
        # Get file content from branch1
        content_branch1 = subprocess.run(
            ["git", "show", f"{branch1}:{file_path}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

        # Get file content from branch2
        content_branch2 = subprocess.run(
            ["git", "show", f"{branch2}:{file_path}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

        # Generate unified diff
        diff = difflib.unified_diff(
            content_branch1,
            content_branch2,
            fromfile=f"{branch1}/{file_path}",
            tofile=f"{branch2}/{file_path}",
            lineterm='',
        )
        return '\n'.join(diff)
    except subprocess.CalledProcessError as e:
        print(f"Error comparing file {file_path} between {branch1} and {branch2}: {e}")
        return None

def main():
    # List of merge request branch names.
    merge_requests = [
        "mr/1",
        "mr/2",
        "mr/3",
        # Add more merge request branches as needed.
    ]

    main_branch = "main"

    # Open the output files.
    with open("present.txt", "w") as present_file, open("not_present.txt", "w") as not_present_file:
        for mr in merge_requests:
            changed_files = get_diff(mr, main_branch)
            if changed_files is None:
                # An error occurred. You might want to log or handle this case differently.
                not_present_file.write(f"{mr} (error comparing branches)\n")
                continue

            if not changed_files or changed_files == ['']:
                # No differences found between mr and main branch.
                present_file.write(f"Merge request {mr} changes are already present in main branch.\n")
                print(f"[PRESENT] {mr} - No diff found against main.")
            else:
                # Differences exist, so the merge request changes are not (completely) in main.
                not_present_file.write(f"{mr}\n")
                print(f"[NOT PRESENT] {mr} - Diff detected.")
                for file in changed_files:
                    diff_output = compare_files(file, main_branch, mr)
                    if diff_output:
                        with open(f"diff_{mr.replace('/', '_')}_{file.replace('/', '_')}.txt", "w") as diff_file:
                            diff_file.write(diff_output)

if __name__ == "__main__":
    main()
