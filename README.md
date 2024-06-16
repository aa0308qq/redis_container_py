# redis_container_py
Using Docker Python SDK to start a Redis container

## Getting Started

### Dependencies

- Docker installed on your machine
- Python and pip installed

### Installing
Use requirements.txt for PyPI installation
```
pip3 install -r requirements.txt
```

## Usage Guide
### Config
Setting up PostgreSQL through YAML
```
image_name: redis:7.2.4
container_name: redis_db
connection_info:
  password: '*******'
  host: '127.0.0.1'
  port: 9527
```
### Library

```
from launcher import pull_image,start,stop
```

### Test
Will automatically pull the Docker image, start the container, and then stop the container

```
python3 launcher.py
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [redis](https://redis.io/docs/latest/commands/)
* [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)
* [docker_python_sdk](https://docker-py.readthedocs.io/en/stable/)
* [pydantic](https://docs.pydantic.dev/latest/)