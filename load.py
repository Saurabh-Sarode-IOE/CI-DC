import random
import time
import threading

class Server:
    def __init__(self, name):
        self.name = name
        self.connections = 0

    def handle_requests(self):
        self.connections +=1
        print(f"{self.name} is handling the request. Active connections: {self.connections}")
        time.sleep(random.uniform(0.5, 1.5))
        self.connections -= 1
        print(f"{self.name} has finished. Active: {self.connections}")

class LoadBalancer:
    def __init__(self, servers, algorithm='round_robin'):
        self.servers = servers
        self.algorithm = algorithm
        self.round_robin_index = 0
    

    def distribute_request(self, client_id):
        if self.algorithm == 'round_robin':
            return self.round_robin(client_id)
        elif self.algorithm == 'least_connections':
            return self.least_connections(client_id)
        
    
    def round_robin(self, client_id):
        server = self.servers[self.round_robin_index]
        print(f"Client {client_id} is sending request to {server.name} (Round Robin)")
        server.handle_requests()
        return server
    
    def least_connections(self, client_id):
        server = min(self.servers, key=lambda s: s.connections)
        print(f"Client {client_id} iss sending to {server.name} (Least Connections)")
        server.handle_requests()
        return server


def simulate_client_requests(client_id, load_balancer):
    for _ in range(random.randint(3, 5)):
        load_balancer.distribute_request(client_id)
        time.sleep(random.uniform(1,3))

def main():
    # Create some server instances
    servers = [Server(f"Server {i+1}") for i in range(3)]  # 3 servers

    # Choose the load balancing algorithm
    lb_algorithm = 'least_connections'  # You can switch this to 'round_robin' to test other algorithm
    load_balancer = LoadBalancer(servers, lb_algorithm)

    # Simulate multiple client requests
    clients = [threading.Thread(target=simulate_client_requests, args=(i+1, load_balancer)) for i in range(5)]  # 5 clients

    # Start all client threads
    for client in clients:
        client.start()

    # Wait for all client threads to finish
    for client in clients:
        client.join()

if __name__ == "__main__":
    main()
