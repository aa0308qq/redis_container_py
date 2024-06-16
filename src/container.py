import os
import time

from docker import errors as docker_errors
from docker.models.containers import Container

from . import utils


def check_container(container_name: str) -> bool:
    with utils.docker_client() as client:
        try:
            client.containers.get(container_name)
        except docker_errors.NotFound:
            return False
        return True


def start_container(
    image_name: str,
    container_name: str,
    password: str,
    port: int,
) -> Container:
    workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_db_path = os.path.join(workspace_path, "storage")
    if check_container(container_name) is True:
        with utils.docker_client() as client:
            container = client.containers.get(container_name)
    else:
        with utils.docker_client() as client:
            try:
                container = client.containers.run(
                    image=image_name,
                    name=f"{container_name}",
                    network_mode="host",
                    volumes=[f"{local_db_path}:/data"],
                    command=[
                        "redis-server",
                        "--save 60 1",
                        "--loglevel warning",
                        "--requirepass",
                        f"{password}",
                        "--port",
                        f"{port}",
                        "--appendonly yes",
                    ],
                    auto_remove=True,
                    detach=True,
                )
                if isinstance(container, Container):
                    while True:
                        check_redis_status = container.exec_run(
                            f"redis-cli -h 127.0.0.1 -p {port} -a {password} ping"
                        )
                        if check_redis_status.exit_code == 0:
                            break
                        else:
                            print(
                                "Waiting,redis is not ready",
                                end="\r",
                                flush=True,
                            )
                        time.sleep(0.01)
            except docker_errors.ContainerError:
                return start_container(
                    image_name,
                    container_name,
                    password,
                    port,
                )
            except docker_errors.APIError as a:
                time.sleep(0.5)
                container = client.containers.get(container_name)
                if not isinstance(container, Container):
                    raise TypeError() from a
                return container
    if not isinstance(container, Container):
        raise TypeError()
    return container


def stop_container(container_name: str) -> bool:
    if check_container(container_name) is True:
        with utils.docker_client() as client:
            container = client.containers.get(container_name)
            if not isinstance(container, Container):
                raise TypeError()
            container.stop()
        return True
    else:
        return False
