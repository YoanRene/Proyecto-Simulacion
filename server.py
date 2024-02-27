import numpy as np

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