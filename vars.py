# Read variables from Terraform file


def get(n) -> str:
    # n  - name of the variable
    # returns the value for the given name if found
    with open("terraform.tfvars") as values:
        for line in values:
            name, var = line.partition("=")[::2]
            if name.strip() == n:
                return var.strip().replace("\"", "")
    return None
