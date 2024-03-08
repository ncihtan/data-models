import argparse
import json
import os
import re
import yaml
from schematic.schemas.generator import SchemaGenerator


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', required=True,
                        help='Path to Schematic config YAML file')
    parser.add_argument('-s', '--schema_path', required=True,
                        help='Path to schema JSON-LD file')
    parser.add_argument('-o', '--out_dir', default='.',
                        help='Directory to save result')
    return parser.parse_args()


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
    sg = SchemaGenerator(path_to_json_ld=schema_path)
    component_digraph = sg.se.get_digraph_by_edge_type('requiresComponent')
    components = component_digraph.nodes()
    components_to_remove = ['Patient', 'File', 'Publication']
    components = sorted(list(set(components) - set(components_to_remove)))
    mm_graph = sg.se.get_nx_schema()
    display_names = sg.get_nodes_display_names(components, mm_graph)
    for index, component in enumerate(components):
        deps = sg.get_node_dependencies(component)
        schema_type = 'file' if 'Filename' in deps else 'record'
        schemas.append({
            'display_name': display_names[index],
            'schema_name': component,
            'type': schema_type
        })
    return schemas


def sort_manifest_schemas(s):
    """Sorts the schema entries in ascending order"""
    ms = s['manifest_schemas']
    sorted_schemas = sorted(ms, key=lambda schema: (schema['type'], schema['display_name']))
    s['manifest_schemas'] = sorted_schemas
    return s


def main():
    args = get_args()
    config = _parse_schema(args.config_path)
    schema_path = args.schema_path
    schemas_config = generate_schema_config(schema_path)

    config = {
        'manifest_schemas': schemas_config,
        'service_version': '1.0',
        'schema_version': '1.0'
    }
    config = sort_manifest_schemas(config)
    
    output_path = os.path.join(args.out_dir, 'dca-template-config.json')
    with open(output_path, 'w') as o:
        json.dump(config, o, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    main()