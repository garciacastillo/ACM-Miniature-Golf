from sys import exit
from re import search

p=h=None

def ingreso_manual():
    p=ingreso_variable(variable_name(p),0, 2, 500)
    h=ingreso_variable(variable_name(h),0, 1, 50)
    cont_error=0
    while not (2 <= p <= 500 and 1 <= h <= 50) :
        try:
            p=int(input("Ingresar p: "))
            h=int(input("Ingresar h: "))
        except:
            cont_error=cont_error+1
            val_ingreso(cont_error,1)

    puntajes_totales = []
    cont_error=0
    for i in range(p):
        puntajes_persona = []
        for j in range(h):
            puntaje=0
            while  not (1 <= puntaje <= 10**9):
                try:
                    puntaje=int(input(f"Ptje persona {i+1} en el hoyo {j+1}: "))
                except:
                    cont_error=cont_error+1
                    val_ingreso(cont_error,2)
            puntajes_persona.append(puntaje)
        puntajes_totales.append(puntajes_persona)
    return puntajes_totales

def casos_prueba(n):
    global p
    global h
    if n == 1:
        p=h=3
        return [[2,2,2],[4,2,1],[4,4,1]]
    else:
        p=6
        h=4
        return [[3,1,2,2],[4,3,2,2],[6,6,3,2],[7,3,4,3],[3,4,2,4],[2,3,3,5]]

def variable_name(variable):
    from inspect import getframeinfo, currentframe
    for line in getframeinfo(currentframe().f_back)[3]:
        m = search(r'\bvariable_name\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)

def mensajes_error(error, retornar=False, variable_name=None):
    mensaje = ""
    if error == 0:
        mensaje = "Se han ingresados muchos valores errados"
    elif error == 1:
        mensaje = f"Ingrese valor válido para {variable_name}"
    elif error == 2:
        mensaje = "Ingrese valores válidos para los puntajes"
    elif error == 3:
        mensaje = "El valor ingresado no está en el rango correcto"
    mensaje = f'\n>>> Error {error}: '+mensaje+' <<<\n'
    return mensaje if retornar else print(mensaje)

def mensajes(mensaje, variable_name=None, retornar=False):
    if mensaje==0:
        mensaje = f"Ingrese {variable_name}: "
    elif mensaje == 1:
        mensaje = "Desea probar los casos de prueba o manual? \nCaso 1: 1\nCaso 2: 2\nIngreso manual: 3\n"
    return mensaje if retornar else print(mensaje)
        

def error_validate(error_count, error):
    if error_count > 2:
        mensajes_error(0)
        exit()

def is_integer(number):
    return not search('\D',number)

def ingreso_variable(variable_name, mensaje, rango_min=None, rango_max=None):
    loop_count=0
    isInteger = False
    is_in_range = False
    variable=None
    while not isInteger or not is_in_range:
        error_validate(loop_count,0)
        loop_count=loop_count+1
        variable = input(mensajes(mensaje, variable_name, retornar=True))
        isInteger = is_integer(variable)
        if isInteger:
            variable = int(variable)
        else:
            mensajes_error(1, variable_name=variable_name)
            continue
        if rango_min:
            is_in_range = rango_min <= variable <= rango_max
            if not is_in_range:
                mensajes_error(3)
    return variable

def max_calculator(puntajes_totales):
    return max(list(map( lambda x: max(x), puntajes_totales)))

def apply_l(puntajes_totales, l):
    return [ list(map(lambda x: x if x < l else l,i)) for i in puntajes_totales]

def points_sum(puntajes_totales):
    return [sum(item) for item in puntajes_totales]

def values_sum(puntajes_totales,max_value):
    return [points_sum(apply_l(puntajes_totales,l)) for l in range(2,max_value+1)]

def count_unique(matrix):
    return [[sub_list.count(item) for item in sub_list] for sub_list in matrix]

def mix_matriz(matrix1, matrix2):
    return [ list(zip(matrix1[i], matrix2[i])) for i in range(p)]

def sort_set(setlist, pos):
    return sorted(setlist, key=lambda tup: tup[pos])

def set_to_list(setlist):
    return [list(item) for item in setlist]

def traspose_matrix(matrix):
    return list(zip(*matrix.copy()))

def get_ranking(matrix):
    return [ list(sort_set(sublist,1))[0][1] for sublist in matrix]

def calculate_ranking(puntajes_totales):
    max_value = max_calculator(puntajes_totales)
    sum_values = values_sum(puntajes_totales,max_value)
    count_values = count_unique(sum_values)
    final_matrix = mix_matriz(sum_values,count_values)
    result_matrix = []
    for sublist in final_matrix:
        set_list = set(sublist)
        sorted_by_set = sort_set(set_list,0)
        suma = 0
        sublist2 = set_to_list(sublist)
        for i,j in sorted_by_set:
            suma=suma+j
            for item in sublist2:
                if item[0]==i:
                    item[1]=suma
        result_matrix.append(sublist2)
    t_result_matrix = traspose_matrix(result_matrix)
    rankings = get_ranking(t_result_matrix)
    return rankings
        

if __name__ == '__main__':
    option = None
    option = ingreso_variable(variable_name(option), 1, 1,3)
    puntajes_totales = []
    if option < 3:
        puntajes_totales = casos_prueba(option)
    else:
        puntajes_totales = ingreso_manual()

    rankings = calculate_ranking(puntajes_totales)
    print(rankings)
