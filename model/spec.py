from model.imageDef import DockerImageDef
from scripts.docker_info import get_dependency
# imageDefs: an array of imageDefs -> in build order
# build_params_list = list of tuples (path, build_args, img_tag)
# build_params: path -> only provide img name
#               build_args -> provide full -> basetag && dbuild_env
#               img_tag -> provide
# in spec: generate all build args -> pick by docker builder to run

# first loop -> build tree -? fill initial field for imageDef -> dbuild_env, img_tag, name
# second loop -> loop build order -> set isbuilt=true -> imgDependOn: isbuilt == true -> curr tag else query old tag -> if not -> error
#


class builder_spec:
    def __init__(self, yml_dict):

        # TODO: Assertions
        self.imageDefs = {}
        self.plans = {}
        self.img_root = None
        self.parse_build_plans(yml_dict['plans'])
        self.parse_img(yml_dict['images'])
        self.build_params_list = []

    def parse_build_plans(self, plan_specs):
        self.plans = plan_specs

    # set up all imageDefs
    def parse_img(self, image_specs):
        root = None
        images = {}
        for key, image in image_specs.items():
            if key not in images:
                curr_image = DockerImageDef(key)
                images[key] = curr_image
            else:
                curr_image = images[key]
            if 'dbuild_env' in image.keys():
                curr_image.dbuildenv = image['dbuild_env']
            if 'depend_on' in image.keys():
                dep_image_name = image['depend_on']
                if dep_image_name not in images:
                    dep_image = DockerImageDef(dep_image_name)
                    images[dep_image_name] = dep_image
                else:
                    dep_image = images[dep_image_name]
                curr_image.depend_on = dep_image
                dep_image.downstream.append(curr_image)
            else:
                root = images[key]
        assert root is not None
        self.imageDefs = images
        self.img_root = root

    def gen_build_args(self, path, git_suffix, img_modified):
        build_order = self.get_build_order()
        build_args = []
        for imgDef in build_order:
            build_arg = {}
            imgDef.to_build = True
            for plan_name, plan in self.plans.items():
                curr_tag = f"{plan['tag_prefix']}-{self.git_suffix}"
                # get base tag
                if imgDef.depend_on is not None:

                    # if dependent img is built in this run
                    if imgDef.depend_on.to_build:
                        base_tag = curr_tag
                    # get previous tag
                    else:
                        # TODO: throw error if prev tag not present
                        base_full_tag = get_dependency(image_tag)
                        base_tag = base_full_tag.split(':')[1]
                    
                    
            image_tag = f"{image_spec['image_name']}:{tag}"

            

    def get_build_order(self):
        tree_order = self.root.get_level_order()
        image_order = []
        for image in self.images_changed:
            image_def = self.imageDefs[image]
            image_order.append((image_def, tree_order[image_def]))
        image_order.sort(key=lambda x: x[1])
        build_order = []
        for idx in range(len(image_order)):
            curr_image_def = image_order[idx][0]
            if image_order[idx][0] not in build_order:
                build_order += (curr_image_def.subtree_order())
        return build_order

    def __str__(self):
        return f'spec({self.imageDefs},{self.build_params_list})'


# FIXME: will there be more than 1 root?
def build_tree(image_specs):
    root = None
    images = {}
    for key, image in image_specs.items():
        if key not in images:
            curr_image = DockerImageDef(key)
            images[key] = curr_image
        else:
            curr_image = images[key]
        if 'depend_on' in image.keys():
            dep_image_name = image['depend_on']
            if dep_image_name not in images:
                dep_image = DockerImageDef(dep_image_name)
                images[dep_image_name] = dep_image
            else:
                dep_image = images[dep_image_name]
            curr_image.depend_on = dep_image
            dep_image.downstream.append(curr_image)
        else:
            root = images[key]
    assert root is not None
    return images, root

 def get_build_order(specs):
        tree, root = build_tree(specs)
        tree_order = root.get_level_order()
        image_order = []
        for image in self.images_changed:
            image_def = tree[image]
            image_order.append((image_def, tree_order[image_def]))
        image_order.sort(key=lambda x: x[1])
        build_order = []
        for idx in range(len(image_order)):
            curr_image_def = image_order[idx][0]
            if image_order[idx][0] not in build_order:
                build_order += (curr_image_def.subtree_order())
        return build_order


 if 'depend_on' in image_spec:
                if 'image_tag' in self.specs['images'][image_spec['depend_on']]:
                    base_full_tag = self.specs['images'][image_spec['depend_on']]['image_tag']
                else:
                    base_full_tag = get_dependency(image_tag)
                custom_tag = base_full_tag.split(':')[1]
                build_args.update(BASE_TAG=custom_tag)

if __name__ == '__main__':
    spec_dict = {'images': 'images1', 'build_param': 'a=1'}
    builder_1 = builder_spec(spec_dict)
    print(builder_1)
