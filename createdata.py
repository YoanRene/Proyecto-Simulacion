import numpy as np
import pandas as pd
from scipy import stats
from main import simulate_system
import itertools
import json

arrival_distributions = ['exponential','uniform','poisson']
scales = [1]
service_distributions = [
    [
        {'distribution': 'exponential', 'lam': 1},
    ],
    [
        {'distribution': 'exponential', 'lam': 1},
        {'distribution': 'poisson', 'lam': 3},
    ],
    [
        {'distribution': 'exponential', 'lam': 1},
        {'distribution': 'poisson', 'lam': 3},
        {'distribution': 'poisson', 'lam': 3},
    ],
    [
        {'distribution': 'poisson', 'lam': 1},
        {'distribution': 'poisson', 'lam': 1},
    ]

]
num_customers = [1000]
max_time = [1000]
low = [2]
high = [4]
lam = [1.0]

c=itertools.product(arrival_distributions,scales,service_distributions,num_customers,max_time,low,high,lam)

sims = [dict(zip(['arrival_distribution','scale','service_distributions','num_customers','max_time','low','high','lam'],cs)) for cs in c]

# Definir las diferentes configuraciones de simulación
simulations = [
    {
        'arrival_distribution': 'exponential',
        'scale': 1,
        'service_distributions': [
            {'distribution': 'exponential', 'lam': 1},
            {'distribution': 'poisson', 'lam': 3},
        ],
        'num_customers': 99999,
        'max_time': 1000
    },
    {
        'arrival_distribution': 'uniform',
        'low': 0.5,
        'high': 2.0,
        'service_distributions': [
            {'distribution': 'exponential', 'lam': 1},
            {'distribution': 'poisson', 'lam': 3},
            {'distribution': 'poisson', 'lam': 3},
        ],
        'num_customers': 99999,
        'max_time': 1000
    },
    {
        'arrival_distribution': 'exponential',
        'scale': .5,
        'service_distributions': [
            {'distribution': 'exponential', 'lam': 1},
        ],
        'num_customers': 1000,
        'max_time': 1000
    },
    {
        'arrival_distribution': 'uniform',
        'low': 1.0,
        'high': 3.0,
        'service_distributions': [
            {'distribution': 'poisson', 'lam': 1},
            {'distribution': 'poisson', 'lam': 1},
        ],
        'num_customers': 99999,
        'max_time': 1000
    },
    # Agrega más configuraciones de simulación según tus necesidades
]

# Lista para almacenar los resultados de las simulaciones
sim_num=0
sims_json = {}
# Realizar las simulaciones
for simulation in sims:
    simulation_results = []
    # Ejecutar la simulación 30 veces
    for i in range(30):
        result = simulate_system(**simulation)
        result.pop("servers")
        result.pop("customers")
        # Agregar los resultados a la lista
        simulation_results.append(result)

    # Convertir los resultados en un DataFrame de pandas
    df_results = pd.DataFrame(simulation_results)

    arrival_distribution = f'({simulation['scale']})' if simulation['arrival_distribution'] == 'exponential' else f'({simulation['low']}-{simulation['high']})'
    print(f'-Simulacion de {len(simulation['service_distributions'])} servidores y distribucion de llegada {simulation["arrival_distribution"]} {arrival_distribution}')
    # Ejemplo: Calcular el promedio de tiempo total de todas las simulaciones
    average_total_time = df_results['total_time'].mean()
    print("Promedio de tiempo total:", average_total_time)

    # Ejemplo: Calcular el máximo de clientes atendidos en una simulación
    max_customers_served = df_results['customers_served'].max()
    print("Máximo de clientes atendidos:", max_customers_served)

    # Ejemplo: Calcular el promedio de tiempo de espera promedio de todas las simulaciones
    average_avg_waiting_time = df_results['average_waiting_time'].mean()
    print("Promedio de tiempo de espera promedio:", average_avg_waiting_time)

    # Puedes realizar más análisis estadísticos según tus necesidades

    # Guardar los resultados en un archivo CSV
    df_results.to_csv(f'data2/s_{sim_num}.csv', index=False)
    sims_json[str(sim_num)] = simulation
    sim_num+=1
d = pd.DataFrame(sims_json)
d.to_csv('data2/sims.csv', index=False)
sim_json = json.dumps(sims_json)
with open('data2/sims.json', 'w') as f:
    f.write(sim_json)