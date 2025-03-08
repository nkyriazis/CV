#!/usr/bin/env python3
import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def load_context(context_path):
    if context_path.endswith(('.yml', '.yaml')):
        import yaml  # ensure PyYAML is installed
        with open(context_path, 'r') as f:
            return yaml.safe_load(f)
    else:
        with open(context_path, 'r') as f:
            return json.load(f)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply a Jinja2 template to a LaTeX document."
    )
    parser.add_argument(
        '--template', type=str, required=True,
        help="Path to the Jinja2 template file (LaTeX document)."
    )
    parser.add_argument(
        '--output', type=str, required=True,
        help="Path for the rendered output LaTeX file."
    )
    parser.add_argument(
        '--context', type=str,
        help="Path to a JSON file containing context variables."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    template_dir, template_file = os.path.split(args.template)
    env = Environment(
        loader=FileSystemLoader(template_dir or '.'),
        autoescape=select_autoescape(['tex']),
        # # Simpler delimiters:
        # block_start_string='<%',
        # block_end_string='%>',
        # variable_start_string='<%=',
        # variable_end_string='%>',
        # comment_start_string='<%#',
        # comment_end_string='%>'
    )
    template = env.get_template(template_file)
    context = {}
    if args.context:
        context = load_context(args.context)
    rendered_output = template.render(**context)
    with open(args.output, 'w') as f:
        f.write(rendered_output)
    print(f"Rendered LaTeX written to {args.output}")

if __name__ == "__main__":
    main()
