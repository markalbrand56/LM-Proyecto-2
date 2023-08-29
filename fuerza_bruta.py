def evaluate_clause(clause, assignment):
    for literal in clause:
        variable = literal[0]
        # print(f"variable: {variable}")
        if literal.startswith('-'):
            if variable in assignment and not assignment[variable]:
                return True  # Satisfiable
        else:
            if variable in assignment and assignment[variable]:
                return True  # Satisfiable
    return False  # Unsatisfiable


def evaluate_formula(formula, assignment):
    for clause in formula:
        # print(f"clause: {clause}")
        if not evaluate_clause(clause, assignment):
            return False  # Unsatisfiable
    return True  # Satisfiable


def brute_force_satisfiability(clauses, num_variables):
    variable_names = list(set(variable for clause in clauses for literal in clause for variable in literal.lstrip('-')))
    for i in range(2 ** num_variables):
        assignment = {variable: bool((i >> j) & 1) for j, variable in enumerate(variable_names)}
        # print(f"assignment: {assignment}")
        is_satisfiable = evaluate_formula(clauses, assignment)
        if is_satisfiable:
            return True, assignment
    return False, {}


# Pedir al usuario que ingrese las cláusulas
input_str = input("Ingrese las cláusulas en el formato {{p}, {-q, -r}, ...}: ")
clauses = []
for clause_str in input_str.split(", "):
    if clause_str == '{}':
        continue  # Ignorar cláusulas vacías
    clause = [literal.strip() for literal in clause_str.strip("{}").split(",")]

    for i in range(len(clause)):
        clause[i] = clause[i].strip("{")
        clause[i] = clause[i].strip("}")

    if any(clause):
        print(f"clause: {clause}")
        clauses.append(clause)

print(f"Cláusulas: {clauses}")
# Identificar todas las variables presentes en las cláusulas
variables = set()
for clause in clauses:
    for literal in clause:
        variable = literal.lstrip('-')
        variable = variable.strip('{')
        variable = variable.strip('}')
        variables.add(variable)

num_variables = len(variables)
print(f"Variables: {variables}")
is_satisfiable, assignment = brute_force_satisfiability(clauses, num_variables)

if is_satisfiable:
    print("La fórmula es satisfacible con la asignación:", assignment)
else:
    print("La fórmula no es satisfacible.")
