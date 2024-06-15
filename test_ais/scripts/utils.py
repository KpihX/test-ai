import csv


def sanitize_term(term):
    """
    This will append _ to atoms begining with digits and add quotes to atoms starting with capital letters
    """
    if term[0].isdigit():
        term = "_" + term
    elif term[0].isupper():
        term = term.lower()
    return term


def generate_prolog_predicates(csv_file, predicate_name):
    """
    This collects a csv file and creates a knowledge base <predicate_name>_output.pl. This file will contain a list of facts expressed as follows
    Assume a csv file with N-lines(rows) and M columns
    <predicate_name>(term11, ..., term1M) .
    <predicate_name>(term21, ..., term2M).
    .
    <predicate_name>(termM1, ..., termMM)
    .
    <predicate_name>(termN1, ..., termNM)
    """
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        # Read the first row to determine the number of columns (arity)
        first_row = next(reader)
        arity = len(first_row)

        # Read the rest of the rows
        terms = [first_row] + [row for row in reader if row]

    with open(f"./{predicate_name}_output.pl", mode="w") as file:
        for term in terms:
            # Sanitize each term
            sanitized_terms = [sanitize_term(t) for t in term]
            # Join terms with commas to match Prolog predicate format
            term_str = ", ".join(sanitized_terms)
            file.write(f"{predicate_name}({term_str}).\n")  # Example usage
