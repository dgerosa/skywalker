import ast

def extract_docstrings_from_file(pyfile):
    with open(pyfile, 'r') as f:
        source = f.read()

    parsed = ast.parse(source)
    items = []

    for node in parsed.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            docstring = ast.get_docstring(node)
            items.append((name, docstring))

    return items

def write_markdown(items, mdfile):
    with open(mdfile, 'w') as f:
        for name, docstring in items:
            f.write(f"## `{name}`\n\n")
            if docstring:
                f.write(docstring.strip() + "\n\n")
            else:
                f.write("_No docstring available._\n\n")

if __name__ == "__main__":
    pyfile = 'skywalker/skywalker.py'  # replace with the path to your Python file
    mdfile = 'docs.md'
    items = extract_docstrings_from_file(pyfile)
    write_markdown(items, mdfile)