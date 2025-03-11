import subprocess

import toml

PYPROJECT_FILE = "pyproject.toml"


def get_installed_dependencies():
    """Fetch the list of installed packages using pip freeze."""
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    return [dep.replace("==", ">=") for dep in result.stdout.strip().split("\n")]


def update_pyproject_dependencies():
    """Update the dependencies in pyproject.toml based on installed packages."""
    try:
        # Load existing pyproject.toml
        with open(PYPROJECT_FILE, "r") as file:
            pyproject_data = toml.load(file)

        # Get the installed dependencies
        installed_deps = get_installed_dependencies()

        # Update dependencies section
        if "project" in pyproject_data and "dependencies" in pyproject_data["project"]:
            pyproject_data["project"]["dependencies"] = installed_deps
        else:
            print(
                "Error: pyproject.toml does not have a [project.dependencies] section."
            )
            return

        # Save back to pyproject.toml
        with open(PYPROJECT_FILE, "w") as file:
            toml.dump(pyproject_data, file)

        print(f"✅ Successfully updated dependencies in {PYPROJECT_FILE}!")

    except Exception as e:
        print(f"❌ Failed to update pyproject.toml: {e}")


# Run the update function
if __name__ == "__main__":
    update_pyproject_dependencies()
