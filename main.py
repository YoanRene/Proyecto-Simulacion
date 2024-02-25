import numpy as np
import heapq
import time

#Clase para almacenar los valores de los clientes
class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_time = 0

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
    
    def time_waited(self,current_time):
        #TODO NO se que hacer cuando la simulacion para por tiempo y hay gente en la cola, de momento se calcula con el tiempo final pasado por parametro
        return self.service_time -self.arrival_time if self.service_time!=0 else current_time-self.arrival_time

class Server:
    def __init__(self, service_distribution,**kwargs):
        self.service_distribution = service_distribution
        self.distribution_params = kwargs
        self.current_customer = None
        self.service_end_time = None
        self.idle_time = 0
        self.last_service_time = 0
        self.customers_served = 0
    def __str__(self):
        return f'{self.service_distribution}, {self.distribution_params}'
    def is_busy(self):
        return self.current_customer is not None

    def start_service(self, customer, current_time):
        self.customers_served +=1
        customer.service_time = current_time
        self.current_customer = customer
        service_time = self.generate_service_time()
        self.service_end_time = current_time + service_time
        self.idle_time += current_time - self.last_service_time
        self.last_service_time = self.service_end_time
        return service_time

    def end_service(self):
        service_time = self.service_end_time - self.current_customer.arrival_time
        self.current_customer = None
        self.service_end_time = None
        return service_time
    def generate_service_time(self):
        if self.service_distribution == 'exponential':
            lam = self.distribution_params.get('lam', 1.0)
            return np.random.exponential(scale=1.0 / lam)
        elif self.service_distribution == 'poisson':
            lam = self.distribution_params.get('lam', 1.0)
            return np.random.poisson(lam=lam)
        elif self.service_distribution == 'normal':
            loc = self.distribution_params.get('loc', 1.0)
            scale = self.distribution_params.get('scale', 0.1)
            return abs(np.random.normal(loc=loc, scale=scale))
        else:
            raise ValueError('Invalid distribution specified')
def simulate_system(arrival_distribution, service_distributions, num_customers,max_time):
    #Empezamos con una lista vacia de clientes y el tiempo en 0
    customers = []
    customers_queue = []
    heapq.heapify(customers_queue)
    current_time = 0
    max_queue =0
    sum_queue = 0
    count_queue = 0

    #Inicializamos los servidores
    servers = []
    for distribution_params in service_distributions:
        distribution = distribution_params['distribution']
        kwargs = {k: v for k, v in distribution_params.items() if k != 'distribution'}
        server = Server(distribution, **kwargs)
        servers.append(server)

    #Genera el valor del proximo arrivo siguiendo la distribucion exponencial
    def get_next_arrival_time():
        if arrival_distribution == 'exponential':
            return current_time + np.random.exponential(scale=scale)
        elif arrival_distribution == 'uniform':
            return current_time + np.random.uniform(low=low, high=high)
        elif arrival_distribution == 'poisson':
            return current_time + np.random.poisson(lam=lam)
        else:
            raise ValueError('Invalid arrival distribution specified')

    #Retorna el indice del servidor que este libre
    def get_next_service_server():
        available_servers = [i for i, server in enumerate(servers) if not server.is_busy()]
        if len(available_servers) > 0:
            return min(available_servers)
        else:
            return None

    def get_next_service_time(server_index):
        return np.random.choice(servers[server_index].service_distribution)
    #Retorna el cliente con el tiempo de espera mas grande
    def get_longest_waiting_customer():
        if len(customers_queue) > 0:
            return heapq.heappop(customers_queue)
        else:
            return None
    #Obtenemos el tiempo en que llega el primer cliente
    clientes = 0
    next_arrival_time = get_next_arrival_time()
    #Simulamos el sistema hasta que no haya mas clientes y los servidores esten libres
    while (clientes < num_customers or any(server.is_busy() for server in servers)) and current_time< max_time:
        log(f'Time: {current_time}')
        #Verificamos que ocurre primero, si llega un cliente o un servidor termina el servicio
        if next_arrival_time is not None and (next_arrival_time < min(server.service_end_time for server in servers if server.is_busy()))if any(server.is_busy() for server in servers) else True:
            #Si lo primero que pasa es que llega un cliente, actualizamos el tiempo
            current_time = next_arrival_time

            #Si ya no hay clientes, detenemos el sistema
            if clientes >= num_customers:
                next_arrival_time = None
                continue
            log(f'\t-Llega cliente')
            clientes+=1
            #Creamos el cliente y lo ponemos en la lista de clientes
            customer = Customer(current_time)
            customers.append(customer)
            #heapq.heappush(customers, customer)

            #Obtenemos el servidor que este libre y lo asignamos
            server_index = get_next_service_server()
            if server_index is not None:
                log(f'\t-Cliente es atendido en servidor {server_index}\n')
                service_time = servers[server_index].start_service(customer, current_time)
                next_service_end_time = current_time + service_time
                #heapq.heappush(customers, Customer(next_service_end_time))
            else:
                log(f'\t-Cliente en cola\n')
                #Si no hay servidores libres lo ponemos en la cola
                heapq.heappush(customers_queue, customer)
                if len(customers_queue) > max_queue:
                    max_queue = len(customers_queue)
            #Calculamos cuando llegaria el proximo cliente
            next_arrival_time = get_next_arrival_time()
        else:
            #Si lo primero que pasa es que un servidor termina el servicio actualizamos el tiempo
            current_time = min(server.service_end_time for server in servers if server.is_busy())
            #Obtenemos el servidor que termino el servicio
            server_index = np.argmin([server.service_end_time if server.is_busy() else np.inf for server in servers])
            service_time = servers[server_index].end_service()
            log(f'\t-Servidor {server_index} termina servicio')
            #Obtenemos el cliente que lleva mas tiempo en la cola
            longest_waiting_customer = get_longest_waiting_customer()
            if longest_waiting_customer is not None:
                log(f'\t-Servidor {server_index} atiende a cliente de la cola\n')
                server_index = get_next_service_server()
                if server_index is not None:
                    service_time = servers[server_index].start_service(longest_waiting_customer, current_time)
                    next_service_end_time = current_time + service_time
                    #heapq.heappush(customers, Customer(next_service_end_tme))
            else:
                log(f'\t-Servidor {server_index} en espera de clientes\n')
        sum_queue+=len(customers_queue)
        count_queue +=1
        if slow:
            time.sleep(0.1)
        #print(f'Tiempo: {round(current_time,3)} \t- Clientes: {clientes} \t- Clientes en cola: {len(customers_queue)}     ',end='\r')
        log(f'Tiempo: {round(current_time,3)} \t- Clientes: {clientes} \t- Clientes en cola: {len(customers_queue)}')

    #return current_time
    waiting_times = [customer.time_waited(current_time) for customer in customers]
    average_waiting_time = sum(waiting_times) / len(waiting_times)
    for s in servers:
        log(f'\nServer {servers.index(s)}({s}):\n\t-Idle time: {round(s.idle_time,2)}({round((s.idle_time/current_time)*100,2)}%)\n\t-Customers served:{s.customers_served}',"servers")
    log(f'\nTotal time: {current_time}')
    customers_served = sum([s.customers_served for s in servers])
    log(f'Clientes Totales:{clientes}',"info")
    log(f'Clientes Atendidos:{customers_served}',"info")
    log(f'Maximo de clientes en cola:{max_queue}',"info")
    log(f'Promedio de clientes en cola:{round(sum_queue/count_queue,2)}',"info")
    log(f'Maximo Tiempo de Espera: {max(waiting_times)}','info')
    log(f"Tiempo de espera promedio: {average_waiting_time}","info")

arrival_distribution = "exponential"
scale=1

#arrival_distribution = "uniform"
low = 1.0
high = 2.0

#arrival_distribution = "poisson"
lam = 1.0

# Distribuciones de servicio en los servidores
service_distributions = [
    {'distribution': 'exponential', 'lam': 1},
    {'distribution': 'poisson', 'lam': 1},
    #{'distribution': 'normal', 'loc': 2.5, 'scale': 8},
    #{'distribution': 'normal', 'loc': 5, 'scale': 10},
    #{'distribution': 'poisson', 'lam': 4},
    #{'distribution': 'exponential', 'lam': .1},
]
#Condiciones de parada
num_customers = 100000
max_time = 1000
debug = False
slow=False
taglist = [
    "servers",
    "info",
    #"initial"
    ]
def log(message,TAG=""):
    if debug or TAG in taglist:
        print(message)
log(f'Simulando {len(service_distributions)} servidores.',"initial")
log(f'Distribucion de llegada: {arrival_distribution}({scale if arrival_distribution == "exponential" else (low, high if arrival_distribution == "uniform" else lam)})',"initial")
log(f'Detener la simulacion despues de atender {num_customers} clientes o pasar 1000 unidades de tiempo',"initial")
log("_____________________________________________________________","initial")
simulate_system(arrival_distribution, service_distributions, num_customers,max_time)
