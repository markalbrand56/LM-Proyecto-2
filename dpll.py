def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]


def dpll(b, assignments={}):
    ## Si B es vacía, entonces regresar True e I
    if len(b) == 0:
        return True, assignments

    ## Si alguna cláusula/disyunción es vacía, entonces regresar False
    if any([len(c) == 0 for c in b]):
        return False, None

    ## Poner en forma positiva
    l = __select_literal(b)


    ## Eliminar todas las clausulas que contengan l en B.
    ## Eliminar las ocurrencias en la clausula complementaria de L en B.
    ## Así, construir B'.
    new_b = [c for c in b if (l, True) not in c]
    new_b = [c.difference({(l, False)}) for c in new_b]
    ## I' = I U DPLL(B', I')
    sat, vals = dpll(new_b, {**assignments, **{l: True}})

    ## Si el resultado de I es verdadero, entonces regresar True e I.
    if sat:
        return sat, vals

    ## Eliminar todas las clausulas que contengan -l en B.
    ## Eliminar las ocurrencias en la clausula complementaria de -L en B.
    ## Así, construir B''.
    new_b = [c for c in b if (l, False) not in c]
    new_b = [c.difference({(l, True)}) for c in new_b]
    ## I'' = I U DPLL(B'', I'')
    sat, vals = dpll(new_b, {**assignments, **{l: False}})
    ## Si el resultado de I es verdadero, entonces regresar True e I.
    if sat:
        return sat, vals

    ## Si no, regresar False
    return False, None


if __name__ == "__main__":
    # Input: Cláusulas
    # {{p, -q}} => [['p', '-q']]
    # {{p}, -{q}} => [['p'], ['-q']]
    # {{-r}, {-q, -r}, {-p, q, -r}, {q}} => [['-r'], ['-q', '-r'], ['-p', 'q', '-r'], ['q']]

    input_str = input("\nIngrese las cláusulas en el formato {{p}, {-q, -r}, ...}: ")
    b = []

    for clause in input_str.split('}, {'):
        clause = clause.replace('{', '').replace('}', '')  # Eliminar llaves
        clause = clause.split(',')  # Separar literales
        clause = [literal.strip() for literal in clause]  # Eliminar espacios en blanco
        b.append(clause)  # Agregar cláusula a la lista

    b = [{(literal[-1], not literal.startswith('-')) for literal in clause} for clause in b]
    print(f"\tClausulas: {b}")

    # Identificar todas las variables presentes en las cláusulas
    variables = set()
    for clause in b:
        for literal in clause:
            variable = literal[0].lstrip('-')
            variables.add(variable)

    print(f"\tVariables: {variables}")

    is_satisfiable, assignment = dpll(b)

    if is_satisfiable:
        print(f"\tSatisfacible: {is_satisfiable}")
        print(f"\tAsignación: {assignment}")
    else:
        print(f"\tSatisfacible: {is_satisfiable}")
        print(f"\tAsignación: {assignment}")
