import docker

def get_greetings():
    return 'Hello World!'

def get_docker_swarm_status():
    nodes = []
    client = docker.from_env()
    try:
        for node in client.nodes.list():
            nodes.append(node.id) 
    except docker.errors.APIError:
        pass
    return nodes
