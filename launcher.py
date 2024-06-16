import os

from docker.models.containers import Container

if __name__ != "__main__":
    from .src import container, image, utils
else:
    from src import container, image, utils


def start() -> Container:
    workspace_path = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(workspace_path, "redis.yaml")
    config = utils.get_config(yaml_path)
    redis_container = container.start_container(
        image_name=config["image_name"],
        container_name=config["container_name"],
        password=config["connection_info"]["password"],
        port=config["connection_info"]["port"],
    )
    return redis_container


def stop() -> bool:
    workspace_path = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(workspace_path, "redis.yaml")
    config = utils.get_config(yaml_path)
    check = container.stop_container(
        container_name=config["container_name"],
    )
    return check


def pull_image() -> bool:
    workspace_path = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(workspace_path, "redis.yaml")
    config = utils.get_config(yaml_path)
    check = image.pull_docker_image(
        image_name=config["image_name"],
    )
    return check


if __name__ == "__main__":
    pull_image()
    start()
    stop()
