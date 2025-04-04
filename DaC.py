def subset_sum_dyv(R, T, i=None):
    """
    Implementación pura del algoritmo Divide y Vencerás para el problema de la suma de subconjuntos.
    Determina si existe un subconjunto de 'R' que sume exactamente 'T'.

    Parámetros:
        R (list): Lista de enteros positivos (ej. [2, 4, 6]).
        T (int): Valor objetivo a alcanzar (ej. 6).
        i (int, opcional): Índice actual (usado en recursión). Por defecto, es el último índice de 'R'.

    Retorna:
        bool: True si existe un subconjunto que suma 'T', False en caso contrario.

    Complejidad:
        Tiempo: O(2^n) (exponencial en el peor caso).
        Espacio: O(n) (profundidad de la pila de recursión).
    """
    # Inicializar el índice si no se proporciona
    if i is None:
        i = len(R) - 1  # Comenzar desde el último elemento
    
    # Casos base
    if T == 0:
        return True  # El subconjunto vacío es solución
    if i < 0 or T < 0:
        return False  # No hay solución posible
    
    # Paso recursivo: Incluir o excluir R[i]
    incluido = subset_sum_dyv(R, T - R[i], i - 1)  # Incluir R[i] y reducir T
    excluido = subset_sum_dyv(R, T, i - 1)         # Excluir R[i], mantener T
    
    # Combinar resultados (basta con que una rama sea True)
    return incluido or excluido


# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Casos de prueba
    conjuntos = [
        ([2, 4, 6], 6),    # True (2 + 4 = 6)
        ([11, 6, 5], 15),  # False
        ([1, 2, 3], 0),    # True (subconjunto vacío)
        ([], 5)            # False (conjunto vacío, T != 0)
    ]
    
    for R, T in conjuntos:
        resultado = subset_sum_dyv(R, T)
        print(f"Conjunto: {R}, Objetivo: {T} -> Existe subconjunto: {resultado}")
