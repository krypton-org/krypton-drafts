# Minimalist GraphQL spec. implementation
# http://spec.graphql.org/June2018

# http://spec.graphql.org/June2018/#sec-Language.Arguments
class Arguments:
    def __init__(self, arguments=None):
        if isinstance(arguments, Arguments):
            self.arguments = arguments.arguments
        if isinstance(arguments, Argument):
            self.arguments = [arguments]
        else:
            self.arguments = arguments

    def __str__(self):
        if not self.arguments:
            return ""
        return "(" + ", ".join(map(str, self.arguments)) + ")"


class Argument:
    def __init__(self, key, value):
        self.key = key
        self.value = Value(value)

    def __str__(self):
        return f"{self.key}: {self.value}"


# http://spec.graphql.org/June2018/#sec-Language.Fields
class Fields:
    def __init__(self, fields=None):
        if isinstance(fields, Fields):
            self.fields = fields.fields
        if isinstance(fields, Field):
            self.fields = [fields]
        else:
            self.fields = fields

    def __str__(self):
        if not self.fields:
            return ""
        return " {\n" + "\n".join(map(str, self.fields)) + "\n}"


class Field:
    def __init__(self, name, arguments=None, fields=None):
        self.name = name
        self.arguments = Arguments(arguments)
        self.fields = Fields(fields)

    def __str__(self):
        return f"{self.name}{self.arguments}{self.fields}"


# http://spec.graphql.org/June2018/#sec-Language.Operations
class Operation:
    name = None

    def __init__(self, fields=None):
        self.fields = Fields(fields)

    def __str__(self):
        return f"{self.name}{self.fields}"


class Query(Operation):
    name = "query"


class Mutation(Operation):
    name = "mutation"


# http://spec.graphql.org/June2018/#Value
class Value:
    def __init__(self, value):
        if isinstance(value, Value):
            self.value = value.value
        self.value = value

    def __str__(self):
        if isinstance(self.value, dict):
            pairs = (f"{k}: {Value(v)}" for k, v in self.value.items())
            return "{" + ", ".join(pairs) + "}"
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return str(self.value)
