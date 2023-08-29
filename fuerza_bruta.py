def evaluate_clause(clause, assignment):
    is_clause_satisfiable = False
    for literal in clause:
        variable = literal.lstrip('-')
        # print(f"variable: {variable} literal {literal}")
        negation = literal.startswith('-')
        if variable in assignment and assignment[variable] == (not negation):
            is_clause_satisfiable = True
            break
    return is_clause_satisfiable


def evaluate_formula(formula, assignment):
    for clause in formula:
        if not evaluate_clause(clause, assignment):
            return False  # Unsatisfiable
    return True  # Satisfiable


def brute_force_satisfiability(clauses, num_variables):
    variable_names = list(set(variable for clause in clauses for literal in clause for variable in literal.lstrip('-')))
    for i in range(2 ** num_variables):
        assignment = {variable: bool((i >> j) & 1) for j, variable in enumerate(variable_names)}
        is_satisfiable = evaluate_formula(clauses, assignment)
        if is_satisfiable:
            return True, assignment
    return False, {}


if __name__ == '__main__':
    while True:
        # Pedir al usuario que ingrese las cláusulas
        input_str = input("Ingrese las cláusulas en el formato {{p}, {-q, -r}, ...}: ")
        clauses = []

        # {{p, -q}} => [['p', '-q']]
        # {{p}, -{q}} => [['p'], ['-q']]
        # {{-r}, {-q, -r}, {-p, q, -r}, {q}} => [['-r'], ['-q', '-r'], ['-p', 'q', '-r'], ['q']]
        for clause in input_str.split('}, {'):
            clause = clause.replace('{', '').replace('}', '')  # Eliminar llaves
            clause = clause.split(',')  # Separar literales
            clause = [literal.strip() for literal in clause]  # Eliminar espacios en blanco
            clauses.append(clause)  # Agregar cláusula a la lista

        print(f"\tClausulas: {clauses}")

        # Identificar todas las variables presentes en las cláusulas
        variables = set()
        for clause in clauses:
            for literal in clause:
                variable = literal.lstrip('-')  # Eliminar negación
                variables.add(variable)

        print(f"\tVariables: {variables}")
        num_variables = len(variables)
        is_satisfiable, assignment = brute_force_satisfiability(clauses, num_variables)

        if is_satisfiable:
            print("La fórmula es satisfacible con la asignación:", assignment)
        else:
            print("La fórmula no es satisfacible.")

