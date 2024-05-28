# HTAN Data Models


## Citation
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7838214.svg)](https://doi.org/10.5281/zenodo.7838214)  
To cite the latest data model use the Zenodo Concept DOI above (resolves to latest version).
DOIs for specific versions can be found on Zenodo.


## Major files

This repository contains 3 major files:

1. **`HTAN.model.csv`**: The CSV representation of the HTAN data model. This file is created by the collective effort of data curators and annotators from a *community* (in this case *HTAN*), and will be used to create a JSON-LD representation of the data model. Imaging data captured by the model adheres to the [Minimum Information about Tissue Imaging (MITI) standard](https://www.miti-consortium.org/).

2. **`HTAN.model.jsonld`** | The JSON-LD representation of the HTAN data model, which is automatically created from the CSV data model using the schematic CLI. More details on how to convert the CSV data model to the JSON-LD data model can be found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). This is the central schema (data model) which will be used to power the generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) from the schema.

3. **`config.yml`** | The schematic-compatible configuration file, which allows users to specify values for application-specific keys (e.g., path to Synapse configuration file) and project-specific keys (e.g., Synapse fileview for community project). A description of what the various keys in this file represent can be found in the [schematic installation guide](https://github.com/Sage-Bionetworks/schematic?tab=readme-ov-file#installation-guide-for-data-curator-app).

## Updating the data model

1. Create and checkout a new branch from `main`. We suggest you work in a branch of this repo rather than on a fork.
     ```
    git checkout -b <your-feature-branch>
    ```
    - Ensure the branch name is descriptive eg `fix-imaging-dimensions`, `rfx-rppa-level-4-v2` or `add-days-validation`.
    - Move the issue status to 'In progress'
3. Locally edit `HTAN.model.csv` to add new features, ensuring careful transcription from an RFC or issue if approriate.
4. If you have created a new component ensure it is added to `dca-template-config.json`
4. Push the change with an informative commit message
    ```
    git add -A
    git commit -m "update data model"
    git push origin <your-feature-branch>
    ```
5. Check that the Github actions to ensure model integrity and update the `HTAN.model.jsonld` has launched, completed and committed into your branch
    - The action can take ~7 mins to run
    - [Monitor the action on Github](https://github.com/ncihtan/data-models/actions)
    - Ensure the actions have all completed with a green tick ✅
    - Ensure that the `github-actions` user has commited into your branch with the message `auto convert to .jsonld`
    - If model integrity tests fail review the errors and implement changes in your branch.
6.  Make a new PR from your feature branch to `main`
    - Assign @adamjtaylor as reviewer
    - Link the PR to the issue
    - Move the issue status to 'ready for review'.
8. Merging is blocked until after review is approved.
    - Through review process if needed update the branch from `main` to ensure alignment with the latest data model.
7. Once merged...
    - Delete the branch to keep things tidy (should be automatic)
    - Move the issue status to 'In staging'

## Data release process

Data releases are made duirng the "Close out party" at the end of our approximatly monthly sprints

1. Draft a new release
    - Create a new tag following [CalVer](https://calver.org/) format `v<YY>.<MM>.MINOR` eg `v24.5.2` for the second release made in May 2024
    - Set the targrt to the `main` branch
    - Generate release notes
    - Save the draft release
2. Review the release with at least one other team member and agree to release
    - Set as the latest release.
    - Issue the release
4. Update Data Curator Confgi:
    - Edit [htan/dca_config.json](https://github.com/Sage-Bionetworks/data_curator_config/blob/prod/HTAN/dca_config.json) file within the [Sage-Bionetworks/data_curator_config](https://github.com/Sage-Bionetworks/data_curator_config) repo
        - Update [data_model_url](https://github.com/Sage-Bionetworks/data_curator_config/blob/d9b9f367ed30b046d113a1973ff256d219913b00/HTAN/dca_config.json#L5) to the latest release
        - Update [template_menu_config_file](https://github.com/Sage-Bionetworks/data_curator_config/blob/d9b9f367ed30b046d113a1973ff256d219913b00/HTAN/dca_config.json#L7) to the latest release
    - Open a PR and assign to @afwillia
    - Deployment to production is complete once this is merged.

