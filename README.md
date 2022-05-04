# HTAN Data Models

## Major files

This repository contains 3 major files:

1. **`HTAN.model.csv`** | The CSV representation of the HTAN data model. This file is created by the collective effort of data curators and annotators from a *community* (in this case *HTAN*), and will be used to create a JSON-LD representation of the data model.


2. **`HTAN.model.jsonld`** | The JSON-LD representation of the HTAN data model, which is automatically created from the CSV data model using the schematic CLI. More details on how to convert the CSV data model to the JSON-LD data model can be found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). This is the central schema (data model) which will be used to power the generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) from the schema.


3. **`config.yml`** | The schematic-compatible configuration file, which allows users to specify values for application-specific keys (e.g., path to Synapse configuration file) and project-specific keys (e.g., Synapse fileview for community project). A description of what the various keys in this file represent can be found in the [Fill in Configuration File(s)](https://sage-schematic.readthedocs.io/en/develop/README.html#fill-in-configuration-file-s) section of the schematic [docs](https://sage-schematic.readthedocs.io/en/develop/index.html).

## Updating the data model

1. Create and checkout a new branch from `main`
     ```
    git checkout -b <your-feature-branch>
    ```
    - Prefix the branch name with `fix-`, `rfc-` or `add-`
    - Ensure the branch name is descriptive eg `fix-imaging-dimensions`, `rfx-rppa-level-4-v2` or `add-days-validation`.
3. Locally edit `HTAN.model.csv` to add new features, ensuring careful transcription from an RFC or issue if approriate.
4. Push the change with an informative commit message
    ```
    git add -A
    git commit -m "update data model"
    git push origin <your-feature-branch>
    ```
5. Check that the Github action to update the `HTAN.model.jsonld` has launched, completed and committed into your branch
    - The action can take ~7 mins to run
    - [Monitor the action on Github](https://github.com/ncihtan/data-models/actions)
    - Ensure the action has completed with a green tick ✅
    - Ensure that the `github-actions` user has commited into your branch with the message `auto convert to .jsonld`
6.  Make a new PR from your feature branch to `main`
    - Assign @elv-sb as reviewer
7. Once merged...
    - Delete the branch to keep things tidy
    - Notify FAIR data team to regenerate the Data Curator App with the updated model
9. If a new component has been added...
    - Create a branch named `add-<component>` in [`ncihtan/HTAN-data-curator`](https://github.com/ncihtan/HTAN-data-curator)
    - Modify `www/config.json` to add the component ensuring the `schema_name` matches the data model `Component` you are adding
    - Push the change
    - Open a PR in [`ncihtan/HTAN-data-curator`](https://github.com/ncihtan/HTAN-data-curator)
    - Assign @elv-sb as reviewer
    - Once approved notify FAIR data team to regenerate Data Curator App with latest component

