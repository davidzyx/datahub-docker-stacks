# think about what build args need ->> generate build args as read in spec dict


# imageDefs: an array of imageDefs -> in build order
# build_params_list = list of tuples (path, build_args, img_tag)
# build_params: path -> only provide img name
#               build_args -> provide full -> basetag && dbuild_env
#               img_tag -> provide
class builder_spec:
    def __init__(self, yml_dict):
        self.imageDefs = yml_dict['images']
        self.build_params_list = yml_dict['build_param']

    def __str__(self):
        return f'spec({self.imageDefs},{self.build_params_list})'


if __name__ == '__main__':
    spec_dict = {'images': 'images1', 'build_param': 'a=1'}
    builder_1 = builder_spec(spec_dict)
    print(builder_1)
