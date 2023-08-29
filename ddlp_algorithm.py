from copy import deepcopy


def DPLL(clauses, assignment):
    # Revisar que la fórmula sea válida
    if not is_valid_formula(clauses):
        print("Fórmula inválida")
        return False, None

    # Caso base: todas las cláusulas son True
    if all(is_true(clause, assignment) for clause in clauses):
        return True, assignment

    # Caso base: hay alguna cláusula vacía
    if has_empty_clause(clauses):
        return False, None

    # Seleccionar una literal no asignada
    literal = select_literal(clauses, assignment)

    if literal is None:
        return False, None

    # Asignar valor True a la literal
    new_clauses = simplify(clauses, literal, True)
    new_assignment = assign(assignment, literal, True)
    satisfied, new_assignment = DPLL(new_clauses, new_assignment)
    if satisfied:
        return True, new_assignment

    # Asignar valor False a la literal
    new_clauses = simplify(clauses, literal, False)
    new_assignment = assign(assignment, literal, False)
    return DPLL(new_clauses, new_assignment)


def is_true(clause, assignment):
    for literal in clause:
        if literal in assignment and assignment[literal]:
            return True
    return False


def has_empty_clause(clauses):
    for clause in clauses:
        if len(clause) == 0:
            return True
    return False


def is_valid_formula(clauses):
    for clause in clauses:
        if not clause:
            return False
    return True


def select_literal(clauses, assignment):
    # Seleccionar primera literal no asignada
    for clause in clauses:
        for literal in clause:
            if literal not in assignment:
                return literal
    return None


def simplify(clauses, literal, value):
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for l in clause:
            if l == literal:
                if value == False:
                    # Eliminar la cláusula
                    break
            elif l == negate(literal):
                if value == True:
                    # Eliminar la cláusula
                    break
            else:
                new_clause.append(l)
        if len(new_clause) > 0:
            new_clauses.append(new_clause)
    return new_clauses


def assign(assignment, literal, value):
    new_assignment = deepcopy(assignment)
    new_assignment[literal] = value
    return new_assignment


def negate(literal):
    if literal.startswith('!'):
        return literal[1:]
    else:
        return '!' + literal


# Programa principal
banner = True
while banner:
    formula = input("\nIngrese la fórmula clausal (separar cláusulas y literales por comas): ")
    if formula == "exit":
        banner = False
        break
    clauses = [set(clause.split(',')) for clause in formula.split('},{')]

    print("Fórmula clausal:", clauses)

    satisfied, assignment = DPLL(clauses, {})
    if satisfied:
        print("La fórmula es SATISFACIBLE")
        print("Interpretación:", assignment)
    else:
        print("La fórmula es INSATISFACIBLE")