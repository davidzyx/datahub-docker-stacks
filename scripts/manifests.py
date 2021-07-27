from genericpath import isfile
from os import path

from yaml import dump

from scripts.utils import read_var, read_dict, store_series, json2series
from scripts.utils import csv_embed_markdown, strip_csv_from_md, csv_concat
from scripts.utils import get_specs
from scripts.docker_runner import DockerRunner
from scripts.git_helper import GitHelper
from scripts.docker_info import get_layers_md_table


def run_outputs(specs, image_key, image=None):
    """
    Run commands listed in manifests according to list
    """
    image_specs = specs['images'][image_key]
    if image is None:
        image = image_specs['image_name']
    manifest_all = specs['manifests']
    manifest_selected = image_specs['manifests']
    
    with DockerRunner(image) as container:
        outputs = []
        for key in manifest_selected:
            if key not in manifest_all.keys():
                continue
            output = DockerRunner.run_simple_command(
                container,
                manifest_all[key]['command']
            )
            description = manifest_all[key]['description']
            outputs.append(dict(description=description, output=output))
    
    return outputs

def run_report(specs, image_key, image=None, output_dir='manifests'):
    image_specs = specs['images'][image_key]
    if image is None:
        image = image_specs['image_name']
    outputs = run_outputs(specs, image_key, image=image)
    expandable_head = """<details>\n<summary>Details</summary>\n"""
    expandable_foot = """</details>\n"""

    sections = []

    sections.append(get_layers_md_table(image))

    for output in outputs:
        is_long_output = output['output'].count('\n') > 30
        if is_long_output:
            sections.append(
f"""
## {output['description']}

{expandable_head}
```
{output['output']}
```
{expandable_foot}

"""
            )
        else:
            sections.append(
f"""
## {output['description']}

```
{output['output']}
```

"""
            )

    stitched = '\n'.join(sections).strip()
    manifest_fn = image.replace('/', '-').replace(':', '-')
    output_path = path.join(output_dir, f"{manifest_fn}.md")
    with open(output_path, 'w') as f:
        f.write(stitched)


def run_manifests():
    images = read_var('IMAGES_BUILT')
    image_deps = json2series(read_dict('image-dependency.json'), 'dep', 'image')
    store_series(image_deps, 'image-dependency')

    # Write image dependency table to wiki
    dep_table_fp = 'wiki/Image Dependency.md'
    if isfile(dep_table_fp):
        old_csv = strip_csv_from_md(dep_table_fp)
        csv_concat(old_csv, 'artifacts/image-dependency.csv', 'artifacts/image-dependency-updated.csv')
        csv_embed_markdown('artifacts/image-dependency-updated.csv', dep_table_fp, 'Image Dependency')
    else:
        csv_embed_markdown('artifacts/image-dependency.csv', dep_table_fp, 'Image Dependency')

    
    specs = get_specs(path.join('images', 'spec.yml'))
    for image in images:
        keys = list(filter(lambda x: x in image, specs['images']))
        assert len(keys) == 1
        image_key = keys[0]
        run_report(specs, image_key, image=image)


