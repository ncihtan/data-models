# HTAN Data Models

This repository contains 3 major files:

1. `HTAN.model.csv`: The CSV representation of the HTAN data model. This file is created by the collective effort of data curators and annotators from a *community* (in this case *HTAN*), and will be used to create a JSON-LD representation of the data model. Imaging data captured by the model adheres to the [Minimum Information about Tissue Imaging (MITI) standard](https://arxiv.org/abs/2108.09499).


2. `HTAN.model.jsonld`: The JSON-LD representation of the HTAN data model, which is automatically created from the CSV data model using the schematic CLI. More details on how to convert the CSV data model to the JSON-LD data model can be found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). This is the central schema (data model) which will be used to power the generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) from the schema.


3. `config.yml`: The schematic-compatible configuration file, which allows users to specify values for application-specific keys (e.g., path to Synapse configuration file) and project-specific keys (e.g., Synapse fileview for community project). A description of what the various keys in this file represent can be found in the [Fill in Configuration File(s)](https://sage-schematic.readthedocs.io/en/develop/README.html#fill-in-configuration-file-s) section of the schematic [docs](https://sage-schematic.readthedocs.io/en/develop/index.html).
