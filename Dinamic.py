'''
    Subset Sum Problem - Programación Dinámica
    
    Christian Echeverría - 221441
    Gustavo Cruz - 22779
'''

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
