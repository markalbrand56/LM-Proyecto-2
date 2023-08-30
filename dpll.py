def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]


def dpll(cnf, assignments={}):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = __select_literal(cnf)

    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None


if __name__ == "__main__":
    # Input: Cláusulas
    # {{p, -q}} => [['p', '-q']]
    # {{p}, -{q}} => [['p'], ['-q']]
    # {{-r}, {-q, -r}, {-p, q, -r}, {q}} => [['-r'], ['-q', '-r'], ['-p', 'q', '-r'], ['q']]

    input_str = input("\nIngrese las cláusulas en el formato {{p}, {-q, -r}, ...}: ")
    cnf = []

    for clause in input_str.split('}, {'):
        clause = clause.replace('{', '').replace('}', '')  # Eliminar llaves
        clause = clause.split(',')  # Separar literales
        clause = [literal.strip() for literal in clause]  # Eliminar espacios en blanco
        cnf.append(clause)  # Agregar cláusula a la lista

    cnf = [{(literal[-1], not literal.startswith('-')) for literal in clause} for clause in cnf]
    print(f"\tClausulas: {cnf}")

    # Identificar todas las variables presentes en las cláusulas
    variables = set()
    for clause in cnf:
        for literal in clause:
            variable = literal[0].lstrip('-')
            variables.add(variable)

    print(f"\tVariables: {variables}")

    is_satisfiable, assignment = dpll(cnf)

    if is_satisfiable:
        print(f"\tSatisfacible: {is_satisfiable}")
        print(f"\tAsignación: {assignment}")
    else:
        print(f"\tSatisfacible: {is_satisfiable}")
        print(f"\tAsignación: {assignment}")
