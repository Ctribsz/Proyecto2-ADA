'''
    Subset Sum Problem - Proyecto 2
    
    Christian Echeverría - 221441
    Gustavo Cruz - 22779
'''

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from Dinamic import subset_sum_pd
from DaC import subset_sum_dyv

# Función para medir tiempos para Programación Dinámica - bottom up
def measure_pd_time(arr, target_sum):
    start_time = time.time()
    result = subset_sum_pd(arr, target_sum)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Función para medir tiempos para Divide y Vencerás
def measure_dyv_time(arr, target_sum):
    start_time = time.time()
    result = (subset_sum_dyv(arr, target_sum), [])  # Para mantener formato consistente
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Función para generar casos de prueba aleatorios
def generate_test_cases(num_cases, max_size, max_value):
    # Genera los casos de prueba, y vamos a usar los mismos en las 2 implementaciones
    test_cases = []
    for i in range(num_cases):
        # Generar tamaño entre 5 y max_size
        size = random.randint(15, max_size)
        # Generar array aleatorio de enteros positivos
        arr = [random.randint(1, max_value) for _ in range(size)]
        
        # Generar un valor objetivo que esté dentro del rango posible
        if random.random() < 0.7:  # 70% de probabilidad de caso solucionable
            subset_size = random.randint(1, min(5, size))
            indices = random.sample(range(size), subset_size)
            target = sum(arr[idx] for idx in indices)
        else:
            # Caso posiblemente no solucionable
            target = random.randint(1, sum(arr))
        
        test_cases.append((arr, target))
    
    return test_cases

def run_experiments():
    # Vamos a utilizar los mismos valores incluso si son aleatorios, cada uno de los algoritmos tendran los mismos valores de entrada
    print("Generando casos de prueba...")
    test_cases = generate_test_cases(30, 30, 100)
    
    sizes = []
    pd_times = []
    dyv_times = []
    targets = []
    results = []
    
    print("Ejecutando experimentos...")
    for i, (arr, target) in enumerate(test_cases):
        print(f"Caso de prueba {i+1}: {len(arr)} elementos, objetivo {target}")
        
        # Medir tiempo para PD (promedio de 3 ejecuciones)
        pd_time_total = 0.0
        for _ in range(3):
            _, pd_time = measure_pd_time(arr, target)
            pd_time_total += pd_time
        pd_time_avg = pd_time_total / 3
        
        # Medir tiempo para DyV (promedio de 3 ejecuciones)
        dyv_time_total = 0.0
        for _ in range(3):
            _, dyv_time = measure_dyv_time(arr, target)
            dyv_time_total += dyv_time
        dyv_time_avg = dyv_time_total / 3
        
        # Guardar resultados
        sizes.append(len(arr))
        pd_times.append(pd_time_avg)
        dyv_times.append(dyv_time_avg)
        targets.append(target)
        
        pd_result, _ = subset_sum_pd(arr, target)
        results.append("Solucionable" if pd_result else "No solucionable")
        
        print(f"  PD: {pd_time_avg:.6f} seg, DyV: {dyv_time_avg:.6f} seg, Resultado: {results[-1]}")
    
    # Imprimir tabla de resultados
    print("\nTabla de resultados:")
    print("--------------------------------------------------------------------------------")
    print("|  Caso  |  Tamaño  |  Target  |     Resultado    |  Tiempo PD  |  Tiempo DyV  |")
    print("--------------------------------------------------------------------------------")
    
    for i in range(len(sizes)):
        print(f"| {i+1:6d} | {sizes[i]:8d} | {targets[i]:8d} | {results[i]:16s} | {pd_times[i]:11.6f} | {dyv_times[i]:11.6f} |")
    
    # Ordenar por tamaño para las gráficas
    sorted_indices = sorted(range(len(sizes)), key=lambda k: sizes[k])
    sorted_sizes = [sizes[i] for i in sorted_indices]
    sorted_pd_times = [pd_times[i] for i in sorted_indices]
    sorted_dyv_times = [dyv_times[i] for i in sorted_indices]
    
    # Generar gráficas
    print("\nGenerando gráficas...")
    
    # Gráfica comparativa de tiempos (con escala logarítmica)
    plt.figure(figsize=(12, 7))
    plt.plot(sorted_sizes, sorted_pd_times, 'o-', color='blue', markersize=6, label='Programación Dinámica')
    plt.plot(sorted_sizes, sorted_dyv_times, 's-', color='red', markersize=6, label='Divide y Vencerás')
    plt.title("Comparación de tiempos de ejecución (escala logarítmica)")
    plt.xlabel("Tamaño del conjunto")
    plt.ylabel("Tiempo (segundos)")
    plt.yscale('log')  # Usar escala logarítmica para mejor visualización
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig("comparison_times.png")
    
    # Gráfica de barras para comparar tiempos por cada caso
    plt.figure(figsize=(15, 8))
    indices = list(range(len(sizes)))
    width = 0.35
    plt.bar([i - width/2 for i in indices], pd_times, width, label='Programación Dinámica', color='blue')
    plt.bar([i + width/2 for i in indices], dyv_times, width, label='Divide y Vencerás', color='red')
    plt.yscale('log')  # Escala logarítmica
    plt.title("Comparación de tiempos por caso (escala logarítmica)")
    plt.xlabel("Caso de prueba")
    plt.ylabel("Tiempo (segundos)")
    plt.xticks(indices, [str(i+1) for i in range(len(sizes))])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    plt.savefig("bars_comparison.png")
    
    # Gráfica de razón de tiempos (DyV/PD)
    plt.figure(figsize=(12, 7))
    time_ratio = [dyv/pd if pd > 0 else 0 for dyv, pd in zip(sorted_dyv_times, sorted_pd_times)]
    plt.plot(sorted_sizes, time_ratio, 'o-', color='purple', markersize=6)
    plt.axhline(y=1.0, color='gray', linestyle='--')
    plt.title("Razón de tiempos (DyV/PD)")
    plt.xlabel("Tamaño del conjunto")
    plt.ylabel("Razón de tiempos (escala logarítmica)")
    plt.yscale('log')  # Escala logarítmica para ver mejor las proporciones
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("time_ratio.png")
    
    plt.close('all')
    
    print("Experimentos completados. Gráficas guardadas como:")
    print("  - comparison_times.png")
    print("  - bars_comparison.png")
    print("  - time_ratio.png")
    
    return sorted_sizes, sorted_pd_times, sorted_dyv_times

def main():
    """Función principal del programa"""
    print("=== Subset Sum Problem - Proyecto 2 ===")
    print("Christian Echeverría - 221441")
    print("Gustavo Cruz - 22779")
    print("=======================================")
    
    continuar = True
    while continuar:
        print("\nSeleccione una opción:")
        print("1. Ejecutar experimentos (30 casos de prueba y generar gráficas)")
        print("2. Ingresar caso personalizado")
        print("3. Salir")
        
        choice = input("Opción: ")
        
        if choice == "1":
            run_experiments()
        elif choice == "2":
            try:
                input_str = input("\nIngrese los elementos del conjunto separados por espacios: ")
                arr = list(map(int, input_str.split()))
                
                target_str = input("Ingrese el valor objetivo: ")
                target = int(target_str)
                
                # Medir y mostrar resultados
                print(f"\nConjunto: {arr}")
                print(f"Objetivo: {target}")
                
                # Programación Dinámica
                _, pd_time = measure_pd_time(arr, target)
                pd_exists, pd_subset = subset_sum_pd(arr, target)
                
                # Divide y Vencerás
                _, dyv_time = measure_dyv_time(arr, target)
                dyv_exists = subset_sum_dyv(arr, target)
                
                # Mostrar resultados
                print("\nResultados:")
                print("---------------------------------------")
                if pd_exists:
                    print(f"PD: Existe solución. Subconjunto: {pd_subset} (suma: {sum(pd_subset)})")
                else:
                    print("PD: No existe solución.")
                print(f"Tiempo PD: {pd_time:.6f} segundos")
                
                print("---------------------------------------")
                if dyv_exists:
                    print("DyV: Existe solución.")
                else:
                    print("DyV: No existe solución.")
                print(f"Tiempo DyV: {dyv_time:.6f} segundos")
                
            except ValueError:
                print("Error: Ingrese solo números enteros.")
        elif choice == "3":
            print("Saliendo del programa...")
            continuar = False
        else:
            print("Opción inválida. Intente de nuevo.")

main()
