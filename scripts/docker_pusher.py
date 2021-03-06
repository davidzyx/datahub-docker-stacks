import docker
import logging
import os

from scripts.utils import read_var, store_var

from typing import Tuple, List, Optional
ImageFulltagPair = Tuple[docker.models.images.Image, str]

logger = logging.getLogger(__name__)


def docker_login(
    client: docker.DockerClient, username: str, password: str,
    registry: Optional[str] = 'https://index.docker.io/v1/'
):
    """
    Log in to a docker registry given username, password and registry (optional)
    """
    logger.info(f'Logging into registry {registry} as {username}')
    r = client.login(username, password, registry=registry)
    if 'Status' in r.keys() and 'succeeded' in r['Status'].lower():
        return True
    raise ValueError(f'Username/password incorrect for registry {registry}')


def push_images(
    client: docker.DockerClient, pairs: List[ImageFulltagPair],
):
    """
    Push a list of images with their full tag names
    """
    images_pushed = []
    for image, full_tag in pairs:

        if ':' not in full_tag:
            repository = full_tag
            tag = 'latest'
        else:
            repository, tag = full_tag.split(':')

        try:
            logger.info(f'Attempting to push {image} to {repository}:{tag}')

            r = client.images.push(
                repository, tag,
                stream=True,
                decode=True,
            )

            for chunk in r:

                logger.info(chunk)

                if 'status' in chunk:
                    # "The push refers to repository XXX_repo"
                    if repository in chunk['status']:
                        print(chunk['status'])
                    
                    # "XXX_tag: digest: sha256:XXX size: XXX"
                    elif tag in chunk['status']:
                        print('\n' + chunk['status'])

                    # regular progress
                    else:
                        print('.', end='')
 
            # push success
            images_pushed.append(full_tag)
            store_var('IMAGES_PUSHED', images_pushed)

        except docker.errors.APIError as e:
            logger.error('Push error')
            raise e


def run_push():
    cli = docker.from_env()
    if docker_login(cli, 'davidzz', os.environ['DOCKERHUB_TOKEN']):
        tags = read_var('IMAGES_BUILT')
        pairs = [
            (cli.images.get(tag), tag)
            for tag in tags
        ]
        push_images(cli, pairs)


if __name__ == '__main__':
    logging.basicConfig(filename='pusher.log', level=logging.INFO)

    cli = docker.from_env()
    push_images(cli, [(cli.images.get('davidzz/datascience-notebook:2021.2-cd82e1c'), 'davidzz/datascience-notebook:2021.2-cd82e1c')])
    # if docker_login(cli, os.environ['DOCKERHUB_USER'], os.environ['DOCKERHUB_TOKEN']):
    #     pairs = [
    #         (cli.images.get('2eaf89f39e53'), 'davidzz/datahub-base-notebook:2021.2-111111'),
    #         (cli.images.get('56e811b67ec6'), 'davidzz/datascience-notebook:2021.2-111111'),
    #     ]
    #     push_images(cli, pairs)

