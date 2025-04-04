'''
    Subset Sum Problem - Proyecto 2

    Christian Echeverría - 221441
    Gustavo Cruz - 22779
'''

import time
import random
import matplotlib.pyplot as plt
import numpy as np

def subset_sum_pd(arr, target_sum):
    """
    Implementación del Problema de la Suma de Subconjuntos usando Programación Dinámica.
    
    Args:
        arr: Lista de números enteros
        target_sum: Valor objetivo a sumar
        
    Returns:
        tuple: (bool, list) - Indica si existe solución y cuál es el subconjunto
    """
    n = len(arr)
    # Crear tabla DP de tamaño (n+1) x (target_sum+1)
    dp = [[False for _ in range(target_sum + 1)] for _ in range(n + 1)]
    
    # Inicializar primera columna como True (siempre podemos formar suma 0)
    for i in range(n + 1):
        dp[i][0] = True
    
    # Llenar la tabla DP de manera bottom-up
    for i in range(1, n + 1):  # Para cada elemento del conjunto
        for j in range(1, target_sum + 1):  # Para cada suma posible
            # Si el elemento actual es mayor que la suma
            if arr[i-1] > j:
                # Mantenemos el resultado sin incluir este elemento
                dp[i][j] = dp[i-1][j]
            else:
                # Decidimos si incluir o no incluir el elemento
                dp[i][j] = dp[i-1][j] or dp[i-1][j - arr[i-1]]
    
    # Verificar si existe solución
    if dp[n][target_sum]:
        # Reconstruir la solución (elementos utilizados)
        subset = []
        i, j = n, target_sum
        
        while i > 0 and j > 0:
            # Si el valor cambió, significa que incluimos este elemento
            if dp[i][j] != dp[i-1][j]:
                subset.append(arr[i-1])
                j -= arr[i-1]  # Reducimos la suma objetivo
            i -= 1  # Pasamos al elemento anterior
        
        return True, subset
    else:
        return False, []

# Funcion para medir tiempos y ponerlos en las graficas
def measure_pd_time(arr, target_sum):
    start_time = time.time()
    result = subset_sum_pd(arr, target_sum)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Funcion para generar casos de prueba aleatorios
def generate_test_cases(num_cases, max_size, max_value):
    test_cases = []
    for i in range(num_cases):
        # Generar tamaño entre 5 y max_size
        size = random.randint(5, max_size)
        # Generar array aleatorio de enteros positivos
        arr = [random.randint(1, max_value) for _ in range(size)]
        
        # Generar un valor objetivo que esté dentro del rango posible
        if random.random() < 0.7:  # 70% de probabilidad de caso solucionable
            subset_size = random.randint(1, min(5, size))
            indices = random.sample(range(size), subset_size)
            target = sum(arr[i] for i in indices)
        else:
            # Caso posiblemente no solucionable
            target = random.randint(1, sum(arr))
        
        test_cases.append((arr, target))
    
    return test_cases

def run_experiments():
    print("Generando casos de prueba...")
    test_cases = generate_test_cases(30, 25, 100)
    
    sizes = []
    pd_times = []
    targets = []
    results = []
    
    print("Ejecutando experimentos...")
    for i, (arr, target) in enumerate(test_cases):
        print(f"Caso de prueba {i+1}: {len(arr)} elementos, objetivo {target}")
        
        pd_time_total = 0.0
        
        for _ in range(3):
            _, pd_time = measure_pd_time(arr, target)
            pd_time_total += pd_time
        
        pd_time_avg = pd_time_total / 3
        
        # Guardar resultados
        sizes.append(len(arr))
        pd_times.append(pd_time_avg)
        targets.append(target)
        
        pd_result, _ = subset_sum_pd(arr, target)
        results.append("Solucionable" if pd_result else "No solucionable")
        
        print(f"  PD: {pd_time_avg:.6f} segundos, Resultado: {results[-1]}")
    
    print("\nTabla de resultados:")
    print("----------------------------------------------------------------")
    print("|  Caso  |  Tamaño  |  Target  |     Resultado    |  Tiempo PD  |")
    print("----------------------------------------------------------------")
    
    for i in range(len(sizes)):
        print(f"| {i+1:6d} | {sizes[i]:8d} | {targets[i]:8d} | {results[i]:16s} | {pd_times[i]:11.6f} |")
    
    # Ordenar por tamaño para las gráficas
    sorted_indices = sorted(range(len(sizes)), key=lambda k: sizes[k])
    sorted_sizes = [sizes[i] for i in sorted_indices]
    sorted_pd_times = [pd_times[i] for i in sorted_indices]
    
    # Generar gráficas
    print("\nGenerando gráficas...")
    
    # Gráfica de tiempos de PD
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_sizes, sorted_pd_times, 'o-', color='blue', markersize=8)
    plt.title("Tiempo de ejecución - Programación Dinámica")
    plt.xlabel("Tamaño del conjunto")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("pd_time.png")
    plt.close()
    
    print("Experimentos completados. Gráfica guardada como:")
    print("  - pd_time.png")
    
    return sorted_sizes, sorted_pd_times

def test_specific_case():
    """Prueba un caso específico"""
    arr = [3, 1, 5, 9, 12]
    target = 8
    
    print("\n--- Probando caso específico ---")
    print(f"Conjunto: {arr}")
    print(f"Objetivo: {target}")
    
    # Probar con Programación Dinámica
    pd_exists, pd_subset = subset_sum_pd(arr, target)
    if pd_exists:
        print(f"PD: Existe solución. Subconjunto: {pd_subset} (suma: {sum(pd_subset)})")
    else:
        print("PD: No existe solución.")

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
        print("2. Probar caso específico ([3, 1, 5, 9, 12] con objetivo 8)")
        print("3. Ingresar caso personalizado")
        print("4. Salir")
        
        choice = input("Opción: ")
        
        if choice == "1":
            run_experiments()
        elif choice == "2":
            test_specific_case()
        elif choice == "3":
            try:
                input_str = input("\nIngrese los elementos del conjunto separados por espacios: ")
                arr = list(map(int, input_str.split()))
                
                target_str = input("Ingrese el valor objetivo: ")
                target = int(target_str)
                
                # Medir y mostrar resultados
                print(f"\nConjunto: {arr}")
                print(f"Objetivo: {target}")
                
                _, pd_time = measure_pd_time(arr, target)
                pd_exists, pd_subset = subset_sum_pd(arr, target)
                
                if pd_exists:
                    print(f"PD: Existe solución. Subconjunto: {pd_subset} (suma: {sum(pd_subset)})")
                else:
                    print("PD: No existe solución.")
                print(f"Tiempo PD: {pd_time:.6f} segundos")
            except ValueError:
                print("Error: Ingrese solo números enteros.")
        elif choice == "4":
            print("Saliendo del programa...")
            continuar = False
        else:
            print("Opción inválida. Intente de nuevo.")

main()
