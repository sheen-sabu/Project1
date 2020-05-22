from docker import APIClient
import docker

class DockerManager:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
        # change the socket file path based on your server. If you are running on a specific linux flavour, you may need to find the 
        # flavour programmatically and then do something like below:
        # { 
        #   "ubuntu": "unix://var/run/docker.sock",
        #   "fedora": "unix://var/run/docker/docker.sock"
        # }
        self.client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.client_env = docker.from_env()

    def docker_version(self):
        version = self.client.version()
        print(version)

    def docker_build(self, tagname):
        response = [line for line in self.client.build(path=self.dockerfile_path, rm=True, tag=tagname)]    
        print(response)
    
    # def docker_get_image(self, tagname, version):
    #     image = self.client.get_image(tagname + ':' + version)
    #     for item in image:
    #         print(item)
    def docker_create_container(self, tagname, version):
        # container_id = self.client.create_container(tagname + ':' + version, ports=[8080],
        #     host_config=self.client.create_host_config(port_bindings={
        #         8080: 8080,
        #     })
        # )
        # return container_id
        container = self.client_env.containers.run(tagname + ':' + version, detach=True,ports={8080:8080})
        return container
    
tagname = 'dockerphpnginx'
version = 'latest'
docker_manager = DockerManager('resources/docker-php-nginx')
docker_manager.docker_version()
docker_manager.docker_build(tagname)
container = docker_manager.docker_create_container(tagname, version)
print(container.logs())

