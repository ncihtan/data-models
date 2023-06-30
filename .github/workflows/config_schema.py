import argparse
import json
import os
import re
import yaml
from schematic.schemas.generator import SchemaGenerator


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', metavar="",
                        required=True, help='path to schematic config ymal file')
    parser.add_argument('-sr', '--service_repo', metavar="",
                        help='repo path to service')
    parser.add_argument('-o', '--out_dir', default='www', metavar="",
                        help='directory to save result')
    parser.add_argument('--overwrite', action='store_true', default=False,
                        help='whether to overwrite the existing config.json')
    return parser.parse_args()


def _is_valid(value, type):
    if type not in ["repo", "location"]:
        raise ValueError('type must be "repo" or "location"')
    pattern = "^([-_.A-z0-9]+\\/){1,2}[-_.A-z0-9]+$" if type == "repo" else "^[-_.A-z0-9]+\\/.*.jsonld$"
    return bool(re.match(pattern, value))


def _parse_schema(config_path):
    """Parse schematic_config.yml file"""
    with open(config_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)["model"]["input"]
            return config
        except yaml.YAMLError as exc:
            print(exc)


def generate_schema_config(schema_path):
    """Generate schema config with corresponding display name"""
    schemas = []
    # get all required data types from data model jsonld
    sg = SchemaGenerator(path_to_json_ld=schema_path)
    component_digraph = sg.se.get_digraph_by_edge_type('requiresComponent')
    components = component_digraph.nodes()
    # get display names for required data types
    mm_graph = sg.se.get_nx_schema()
    display_names = sg.get_nodes_display_names(components, mm_graph)
    # save display_name, schema_name, assay type to list
    for index, component in enumerate(components):
        # get component's dependencies
        deps = sg.get_node_dependencies(component)
        schema_type = 'file' if 'Filename' in deps else 'record'
        schemas.append({
            'display_name': display_names[index],
            'schema_name': component,
            'type': schema_type
        })
    return schemas


def main():
    args = get_args()
    # retrieve schema info from config file
    config = _parse_schema(args.config_path)

    # get the location of the schema
    #if config.get("location") and _is_valid(config.get("location"), "location"):
    #    schema_path = config["location"]
    #else:
    #    raise ValueError(f'No valid "location" value found in "{args.config_path}" \u274C')

    if args.overwrite:
        # get versions for both service and schema
        #service_version = _get_version(args.service_repo)
        #schema_version = config.get("version") or _get_version(config["repo"])
        # generate schema configuration based on *.model.jsonld
        schemas_config = generate_schema_config(schema_path)
        # write out the config.json including versions
        config = {
            'manifest_schemas': schemas_config,
            'service_version': '1',   #service_version,
            'schema_version': '1'     #schema_version
        }
        output_path = os.path.join(args.out_dir, 'config.json')
        with open(output_path, 'w') as o:
            json.dump(config, o, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    main()
