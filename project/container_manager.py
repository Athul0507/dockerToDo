import docker
import time
import sys

class ContainerManager:
    def __init__(self):
        self.client = docker.from_env()
        
    def list_containers(self):
        """List all active containers"""
        containers = self.client.containers.list()
        print("\nActive containers:")
        for container in containers:
            print(f"ID: {container.short_id}, Name: {container.name}, Status: {container.status}")
            
    def check_container_health(self, container_name):
        """Check health status of a specific container"""
        try:
            container = self.client.containers.get(container_name)
            health = container.attrs['State'].get('Health', {}).get('Status', 'N/A')
            print(f"\nContainer {container_name} health status: {health}")
            return health
        except docker.errors.NotFound:
            print(f"Container {container_name} not found")
            return None
            
    def restart_container(self, container_name):
        """Restart a specific container"""
        try:
            container = self.client.containers.get(container_name)
            print(f"\nRestarting container {container_name}")
            container.restart()
            print("Container restarted successfully")
        except docker.errors.NotFound:
            print(f"Container {container_name} not found")
            
    def monitor_containers(self):
        """Monitor containers and restart unhealthy ones"""
        while True:
            self.list_containers()
            health = self.check_container_health('project-webapp-1')
            
            if health == 'unhealthy':
                print("Webapp container is unhealthy, restarting...")
                self.restart_container('project-webapp-1')
                
            time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    manager = ContainerManager()
    try:
        manager.monitor_containers()
    except KeyboardInterrupt:
        print("\nStopping container monitoring...")
        sys.exit(0)
