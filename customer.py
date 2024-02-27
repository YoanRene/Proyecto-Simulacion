class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_time = 0

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
    
    def time_waited(self,current_time):
        #TODO NO se que hacer cuando la simulacion para por tiempo y hay gente en la cola, de momento se calcula con el tiempo final pasado por parametro
        return self.service_time -self.arrival_time if self.service_time!=0 else current_time-self.arrival_time