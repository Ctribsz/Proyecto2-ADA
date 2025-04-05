def subset_sum_dyv(R, T, i=None):
    if i is None:
        i = len(R) - 1 
    
    # Casos base
    if T == 0:
        return True  
    if i < 0 or T < 0:
        return False  
    
    # Paso recursivo: Incluir o excluir R[i]
    incluido = subset_sum_dyv(R, T - R[i], i - 1)  
    excluido = subset_sum_dyv(R, T, i - 1)
    
    return incluido or excluido


if __name__ == "__main__":
    conjuntos = [
        ([2, 4, 6], 6),    # True (2 + 4 = 6)
        ([11, 6, 5], 15),  # False
        ([1, 2, 3], 0),    # True (subconjunto vacío)
        ([], 5)            # False (conjunto vacío, T != 0)
    ]
    
    for R, T in conjuntos:
        resultado = subset_sum_dyv(R, T)
        print(f"Conjunto: {R}, Objetivo: {T} -> Existe subconjunto: {resultado}")
