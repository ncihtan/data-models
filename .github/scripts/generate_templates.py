import os
import yaml
import json
import pandas as pd
from git import Repo

# Configurations
DATA_MODELS_PATH = "data-models"  # Path to your data models folder
TEMPLATES_OUTPUT_PATH = "data-models/templates"  # Path to save generated templates
GIT_REPO_PATH = "."  # Root of your git repo
BRANCH_NAME = "main"  # Target branch for pushing changes
COMMIT_MESSAGE = "Auto-generate blank templates for latest data model release"


def load_data_model(file_path):
    """Load data model based on its file extension."""
    ext = os.path.splitext(file_path)[1]
    if ext == ".yaml" or ext == ".yml":
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    elif ext == ".json":
        with open(file_path, "r") as f:
            return json.load(f)
    elif ext == ".csv":
        return pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def generate_blank_template(schema):
    """Generate a blank template based on the data model schema."""
    if isinstance(schema, dict):  # For YAML/JSON structured schema
        columns = schema.get("fields", [])
        return pd.DataFrame(columns=[col["name"] for col in columns])
    elif isinstance(schema, pd.DataFrame):  # For CSV schemas
        return pd.DataFrame(columns=schema.columns)
    else:
        raise ValueError("Unsupported schema format")


def save_template(template, output_path):
    """Save the generated template to a CSV file."""
    template.to_csv(output_path, index=False)


def push_to_repo(repo_path, branch, commit_message):
    """Push changes to the Git repository."""
    repo = Repo(repo_path)
    repo.git.add(A=True)
    if repo.is_dirty():
        repo.index.commit(commit_message)
        origin = repo.remote(name="origin")
        origin.push(branch)
    else:
        print("No changes to commit.")


def main():
  if not os.path.exists(TEMPLATES_OUTPUT_PATH):
      os.makedirs(TEMPLATES_OUTPUT_PATH)

  for root, _, files in os.walk(DATA_MODELS_PATH):
      for file in files:
          file_path = os.path.join(root, file)
          try:
              schema = load_data_model(file_path)
              blank_template = generate_blank_template(schema)
              output_file = os.path.join(
                  TEMPLATES_OUTPUT_PATH, os.path.splitext(file)[0] + "_template.csv"
              )
              save_template(blank_template, output_file)
              print(f"Generated template for {file}")
          except Exception as e:
              print(f"Failed to process {file}: {e}")


if __name__ == "__main__":
    main()
