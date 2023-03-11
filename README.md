# (py)illogical

A micro conditional engine used to parse the logical and comparison expressions, evaluate an expression in data context, and provide access to a text form of the given expression.

> Revision: Mar 10, 2023.

Other implementations:
- [TS/JS](https://github.com/spaceavocado/illogical)
- [GO](https://github.com/spaceavocado/goillogical)

## About

This project has been developed to provide Python implementation of [spaceavocado/illogical](https://github.com/spaceavocado/illogical).


## Getting Started

You can install the **(py)illogical** from [PyPI](https://pypi.org/project/illogical/):

```sh
python -m pip install illogical
```

The reader is supported on Python 3.7 and above.

**Table of Content**

---

- [(py)illogical](#pyillogical)
  - [About](#about)
  - [Getting Started](#getting-started)
  - [Basic Usage](#basic-usage)
    - [Evaluate](#evaluate)
    - [Statement](#statement)
    - [Parse](#parse)
    - [Evaluable](#evaluable)
      - [Simplify](#simplify)
      - [Serialize](#serialize)
  - [Working with Expressions](#working-with-expressions)
    - [Evaluation Data Context](#evaluation-data-context)
      - [Accessing Array Element:](#accessing-array-element)
      - [Accessing Array Element via Reference:](#accessing-array-element-via-reference)
      - [Nested Referencing](#nested-referencing)
      - [Composite Reference Key](#composite-reference-key)
      - [Data Type Casting](#data-type-casting)
    - [Operand Types](#operand-types)
      - [Value](#value)
      - [Reference](#reference)
      - [Collection](#collection)
    - [Comparison Expressions](#comparison-expressions)
      - [Equal](#equal)
      - [Not Equal](#not-equal)
      - [Greater Than](#greater-than)
      - [Greater Than or Equal](#greater-than-or-equal)
      - [Less Than](#less-than)
      - [Less Than or Equal](#less-than-or-equal)
      - [In](#in)
      - [Not In](#not-in)
      - [Prefix](#prefix)
      - [Suffix](#suffix)
      - [Overlap](#overlap)
      - [None](#none)
      - [Present](#present)
    - [Logical Expressions](#logical-expressions)
      - [And](#and)
      - [Or](#or)
      - [Nor](#nor)
      - [Xor](#xor)
      - [Not](#not)
  - [Engine Options](#engine-options)
    - [Reference Serialize Options](#reference-serialize-options)
      - [From](#from)
      - [To](#to)
    - [Collection Serialize Options](#collection-serialize-options)
      - [Escape Character](#escape-character)
    - [Simplify Options](#simplify-options)
      - [Ignored Paths](#ignored-paths)
      - [Ignored Paths RegEx](#ignored-paths-regex)
    - [Operator Mapping](#operator-mapping)
  - [Contributing](#contributing)
  - [License](#license)

---


## Basic Usage

```py
from illogical.illogical import Illogical

# Create a new instance of the engine
illogical = Illogical()

# Evaluate an expression
illogical.evaluate(["==", 1, 1], {})
```

> For advanced usage, please [Engine Options](#engine-options).

### Evaluate

Evaluate comparison or logical expression:

`illogical.evaluate(`[Comparison Expression](#comparison-expressions) or [Logical Expression](#logical-expressions), [Evaluation Data Context](#evaluation-data-context)`)` => `bool`

**Example**

```py
context = {
  "name": "peter",
}

# Comparison expression
illogical.evaluate(["==", 5, 5], context)
illogical.evaluate(["==", "circle", "circle"], context)
illogical.evaluate(["==", True, True], context)
illogical.evaluate(["==", "$name", "peter"], context)
illogical.evaluate(["NIL", "$RefA"], context)

# Logical expression
illogical.evaluate(["AND", ["==", 5, 5], ["==", 10, 10]], context)
illogical.evaluate(["AND", ["==", "circle", "circle"], ["==", 10, 10]], context)
illogical.evaluate(["OR", ["==", "$name", "peter"], ["==", 5, 10]], context)
```

### Statement

Get expression string representation:

`illogical.statement(`[Comparison Expression](#comparison-expressions) or [Logical Expression](#logical-expressions)`)` => `str`

**Example**

```py
# Comparison expression

illogical.statement(["==", 5, 5])
# (5 == 5)

illogical.statement(["==", "circle", "circle"])
# ("circle" == "circle")

illogical.statement(["==", True, True])
# (True == True)

illogical.statement(["==", "$name", "peter"])
# ({name} == "peter")

illogical.statement(["NIL", "$RefA"])
# ({RefA} <is nil>)

# Logical expression

illogical.statement(["AND", ["==", 5, 5], ["==", 10, 10]])
# ((5 == 5) AND (10 == 10))

illogical.statement(["AND", ["==", "circle", "circle"], ["==", 10, 10]])
# (("circle" == "circle") AND (10 == 10))

illogical.statement(["OR", ["==", "$name", "peter"], ["==", 5, 10]])
# (({name} == "peter") OR (5 == 10))
```

### Parse

Parse the expression into a **Evaluable** object, i.e. it returns the parsed self-evaluable condition expression.

`illogical.parse(`[Comparison Expression](#comparison-expressions) or [Logical Expression](#logical-expressions)`)` => `Evaluable`

### Evaluable

- `evaluable.evaluate(context)` please see [Evaluation Data Context](#evaluation-data-context).
- `evaluable.simplify(context)` please see [Simplify](#simplify).
- `evaluable.serialize()` please see [Serialize](#serialize).
- `str(evaluable) | evaluable.__str__()` please see [Statement](#statement).

**Example**

```py
evaluable = illogical.parse(["==", "$name", "peter"])

evaluable.evaluate({"name": "peter"})
# True

print(evaluable)
# ({name} == "peter")
```

#### Simplify

Simplifies an expression with a given context. This is useful when you already have some of
the properties of context and wants to try to evaluate the expression.

**Example**

```py
evaluable = illogical.parse(["AND", ["==", "$a", 10], ["==", "$b", 20]])

evaluable.simplify({"a": 10})
# ({b} == 20)

evaluable.simplify({"a": 20})
# False
```

Values not found in the context will cause the parent operand not to be evaluated and returned
as part of the simplified expression.

In some situations we might want to evaluate the expression even if referred value is not
present. You can provide a list of keys that will be strictly evaluated even if they are not
present in the context.

**Example**

```py
from illogical.illogical import Illogical
from illogical.parser.parse import Options

ignored_paths = ["ignored"],
ignored_path_rx = [r"^ignored"],

illogical = Illogical(Options(ignored_paths=ignored_paths, ignored_path_rx=ignored_path_rx))

evaluable = illogical.parse(["AND", ["==", "$a", 10], ["==", "$ignored", 20]])

evaluable.simplify({"a": 10})
# False
# $ignored" will be evaluated to None.
```

Alternatively we might want to do the opposite and strictly evaluate the expression for all referred
values not present in the context except for a specified list of optional keys.

**Example**

```py
from illogical.illogical import Illogical
from illogical.parser.parse import Options

ignored_paths = ["b"]

illogical = Illogical(Options(ignored_paths=ignored_paths))

evaluable = illogical.parse(["OR", ["==", "$a", 10], ["==", "$b", 20}, ["==", "$c", 20]])

evaluable.simplify({"c": 10})
# ({a} == 10)
# except for "$b" everything not in context will be evaluated to None.
```

#### Serialize

Serializes an expression into the raw expression form, reverse the parse operation.

**Example**

```py
evaluable = illogical.parse(["AND", ["==", "$a", 10], ["==", 10, 20]])

evaluable.serialize()
# ["AND", ["==", "$a", 10], ["==", 10, 20]]
```

## Working with Expressions

### Evaluation Data Context

The evaluation data context is used to provide the expression with variable references, i.e. this allows for the dynamic expressions. The data context is object with properties used as the references keys, and its values as reference values.

> Valid reference values: dist, str, int, float, list; set; tuple of (bool, string, int, float).

To reference the nested reference, please use "." delimiter, e.g.:
`$address.city`

#### Accessing Array Element:

`$options[1]`

#### Accessing Array Element via Reference:

`$options[{index}]`

- The **index** reference is resolved within the data context as an array index.

#### Nested Referencing

`$address.{segment}`

- The **segment** reference is resolved within the data context as a property key.

#### Composite Reference Key

`$shape{shapeType}`

- The **shapeType** reference is resolved within the data context, and inserted into the outer reference key.
- E.g. **shapeType** is resolved as "**B**" and would compose the **$shapeB** outer reference.
- This resolution could be n-nested.

#### Data Type Casting

`$payment.amount.(Type)`

Cast the given data context into the desired data type before being used as an operand in the evaluation.

> Note: If the conversion is invalid, then a warning message is being logged.

Supported data type conversions:

- .(String): cast a given reference to String.
- .(Number): cast a given reference to Number.
- .(Integer): cast a given reference to Integer.
- .(Float): cast a given reference to Float.
- .(Boolean): cast a given reference to Boolean.

**Example**

```py
# Data context
context = {
  "name":    "peter",
  "country": "canada",
  "age":     21,
  "options": [1, 2, 3],
  "address": {
    city:    "Toronto",
    country: "Canada",
  },
  "index":     2,
  "segment":   "city",
  "shapeA":    "box",
  "shapeB":    "circle",
  "shapeType": "B",
}

# Evaluate an expression in the given data context

illogical.evaluate([">", "$age", 20], context)
# True

illogical.evaluate(["==", "$address.city", "Toronto"], context)
# True

# Accessing Array Element
illogical.evaluate(["==", "$options[1]", 2], context)
# True

# Accessing Array Element via Reference
illogical.evaluate(["==", "$options[{index}]", 3], context)
# True

# Nested Referencing
illogical.evaluate(["==", "$address.{segment}", "Toronto"], context)
# True

# Composite Reference Key
illogical.evaluate(["==", "$shape{shapeType}", "circle"], context)
# True

# Data Type Casting
illogical.evaluate(["==", "$age.(String)", "21"], context)
# True
```

### Operand Types

The [Comparison Expression](#comparison-expression) expect operands to be one of the below:

#### Value

Simple value types: string, int, float, bool, None.

**Example**

```py
val1 = 5
var2 = "cirle"
var3 = True

illogical.parse(["AND", ["==", val1, var2], ["==", var3, var3]])
```

#### Reference

The reference operand value is resolved from the [Evaluation Data Context](#evaluation-data-context), where the the operands name is used as key in the context.

The reference operand must be prefixed with `$` symbol, e.g.: `$name`. This might be customized via [Reference Predicate Parser Option](#reference-predicate).

**Example**

| Expression                    | Data Context      |
| ----------------------------- | ----------------- |
| `["==", "$age", 21]`          | `{age: 21}`       |
| `["==", "circle", "$shape"] ` | `{shape: "circle"}` |
| `["==", "$visible", True]`    | `{visible: True}` |

#### Collection

The operand could be an array mixed from [Value](#value) and [Reference](#reference).

**Example**

| Expression                               | Data Context                        |
| ---------------------------------------- | ----------------------------------- |
| `["IN", [1, 2], 1]`                      | `{}`                                |
| `["IN", "circle", ["$shapeA", "$shapeB"] ` | `{shapeA: "circle", shapeB: "box"}` |
| `["IN", ["$number", 5], 5]`                | `{number: 3}`                       |

### Comparison Expressions

#### Equal

Expression format: `["==", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string, int, float, bool, None.

```json
["==", 5, 5]
```

```py
illogical.evaluate(["==", 5, 5], context)
# True
```

#### Not Equal

Expression format: `["!=", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string, int, float, bool, None.

```json
["!=", "circle", "square"]
```

```py
illogical.evaluate(["!=", "circle", "square"], context)
# True
```

#### Greater Than

Expression format: `[">", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: int, float.

```json
[">", 10, 5]
```

```py
illogical.evaluate([">", 10, 5], context)
# True
```

#### Greater Than or Equal

Expression format: `[">=", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: int, float.

```json
[">=", 5, 5]
```

```py
illogical.evaluate([">=", 5, 5], context)
# True
```

#### Less Than

Expression format: `["<", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: int, float.

```json
["<", 5, 10]
```

```py
illogical.evaluate(["<", 5, 10], context)
# True
```

#### Less Than or Equal

Expression format: `["<=", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: int, float.

```json
["<=", 5, 5]
```

```py
illogical.evaluate(["<=", 5, 5], context)
# True
```

#### In

Expression format: `["IN", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string, int, float, bool, None and list; set; tuple of (string, int, float, bool, None).

```json
["IN", 5, [1, 2, 3, 4, 5]]
["IN", ["circle", "square", "triangle"], "square"]
```

```py
illogical.evaluate(["IN", 5, [1, 2, 3, 4, 5]], context)
# True

illogical.evaluate(["IN", ["circle", "square", "triangle"], "square"], context)
# True
```

#### Not In

Expression format: `["NOT IN", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string, int, float, bool, None and list; set; tuple of (string, int, float, bool, None).

```json
["IN", 10, [1, 2, 3, 4, 5]]
["IN", ["circle", "square", "triangle"], "oval"]
```

```py
illogical.evaluate(["NOT IN", 10, [1, 2, 3, 4, 5]], context)
# True

illogical.evaluate(["NOT IN", ["circle", "square", "triangle"], "oval"], context)
# True
```

#### Prefix

Expression format: `["PREFIX", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string.

- Left operand is the PREFIX term.
- Right operand is the tested word.

```json
["PREFIX", "hemi", "hemisphere"]
```

```py
illogical.evaluate(["PREFIX", "hemi", "hemisphere"], context)
# True

illogical.evaluate(["PREFIX", "hemi", "sphere"], context)
# False
```

#### Suffix

Expression format: `["SUFFIX", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: string.

- Left operand is the tested word.
- Right operand is the SUFFIX term.

```json
["SUFFIX", "establishment", "ment"]
```

```py
illogical.evaluate(["SUFFIX", "establishment", "ment"], context)
# True

illogical.evaluate(["SUFFIX", "establish", "ment"], context)
# False
```

#### Overlap

Expression format: `["OVERLAP", `[Left Operand](#operand-types), [Right Operand](#operand-types)`]`.

> Valid operand types: list; set; tuple of (string, int, float, bool, None).

```json
["OVERLAP", [1, 2], [1, 2, 3, 4, 5]]
["OVERLAP", ["circle", "square", "triangle"], ["square"]]
```

```py
illogical.evaluate(["OVERLAP", [1, 2, 6], [1, 2, 3, 4, 5]], context)
# True

illogical.evaluate(["OVERLAP", ["circle", "square", "triangle"], ["square", "oval"]], context)
# True
```

#### None

Expression format: `["NONE", `[Reference Operand](#reference)`]`.

```json
["NONE", "$RefA"]
```

```py
illogical.evaluate(["NONE", "RefA"], {})
# True

illogical.evaluate(["NONE", "RefA"], {"RefA": 10})
# False
```

#### Present

Evaluates as FALSE when the operand is UNDEFINED or NULL.

Expression format: `["PRESENT", `[Reference Operand](#reference)`]`.

```json
["PRESENT", "$RefA"]
```

```py
illogical.evaluate(["PRESENT", "RefA"], {})
# False

illogical.evaluate(["PRESENT", "RefA"], {"RefA": 10})
# True

illogical.evaluate(["PRESENT", "RefA"], {"RefA": False})
# True

illogical.evaluate(["PRESENT", "RefA"], {"RefA": "val"})
# True
```

### Logical Expressions

#### And

The logical AND operator returns the bool value TRUE if both operands are TRUE and returns FALSE otherwise.

Expression format: `["AND", Left Operand 1, Right Operand 2, ... , Right Operand N]`.

> Valid operand types: [Comparison Expression](#comparison-expressions) or [Nested Logical Expression](#logical-expressions).

```json
["AND", ["==", 5, 5], ["==", 10, 10]]
```

```py
illogical.evaluate(["AND", ["==", 5, 5], ["==", 10, 10]], context)
# True
```

#### Or

The logical OR operator returns the bool value TRUE if either or both operands is TRUE and returns FALSE otherwise.

Expression format: `["OR", Left Operand 1, Right Operand 2, ... , Right Operand N]`.

> Valid operand types: [Comparison Expression](#comparison-expressions) or [Nested Logical Expression](#logical-expressions).

```json
["OR", ["==", 5, 5], ["==", 10, 5]]
```

```py
illogical.evaluate(["OR", ["==", 5, 5], ["==", 10, 5]], context)
# True
```

#### Nor

The logical NOR operator returns the bool value TRUE if both operands are FALSE and returns FALSE otherwise.

Expression format: `["NOR", Left Operand 1, Right Operand 2, ... , Right Operand N]`

> Valid operand types: [Comparison Expression](#comparison-expressions) or [Nested Logical Expression](#logical-expressions).

```json
["NOR", ["==", 5, 1], ["==", 10, 5]]
```

```py
illogical.evaluate(["NOR", ["==", 5, 1], ["==", 10, 5]], context)
# True
```

#### Xor

The logical NOR operator returns the bool value TRUE if both operands are FALSE and returns FALSE otherwise.

Expression format: `["XOR", Left Operand 1, Right Operand 2, ... , Right Operand N]`

> Valid operand types: [Comparison Expression](#comparison-expressions) or [Nested Logical Expression](#logical-expressions).

```json
["XOR", ["==", 5, 5], ["==", 10, 5]]
```

```py
illogical.evaluate(["XOR", ["==", 5, 5], ["==", 10, 5]], context)
# True
```

```json
["XOR", ["==", 5, 5], ["==", 10, 10]]
```

```py
illogical.evaluate(["XOR", ["==", 5, 5], ["==", 10, 10]], context)
# False
```

#### Not

The logical NOT operator returns the bool value TRUE if the operand is FALSE, TRUE otherwise.

Expression format: `["NOT", Operand]`

> Valid operand types: [Comparison Expression](#comparison-expressions) or [Nested Logical Expression](#logical-expressions).

```json
["NOT", ["==", 5, 5]]
```

```py
illogical.evaluate(["NOT", ["==", 5, 5]], context)
# True
```

## Engine Options

### Reference Serialize Options

**Usage**

```py

from illogical.illogical import Illogical
from illogical.parser.parse import Options

illogical = Illogical(Options(reference_from=reference_from, reference_to=reference_to))
```

#### From

A function used to determine if the operand is a reference type, otherwise evaluated as a static value.

```py
Callable[[str], str]
```

**Return value:**

- `True` = reference type
- `False` = value type

**Default reference predicate:**

> The `$` symbol at the begging of the operand is used to predicate the reference type., E.g. `$State`, `$Country`.

#### To

A function used to transform the operand into the reference annotation stripped form. I.e. remove any annotation used to detect the reference type. E.g. "$Reference" => "Reference".

```py
Callable[[str], str]
```

> **Default reference transform:**
> It removes the `$` symbol at the begging of the operand name.

### Collection Serialize Options

**Usage**

```py
from illogical.illogical import Illogical
from illogical.parser.parse import Options

escape_character = "\\"

illogical = Illogical(Options(escape_character=escape_character))
```

#### Escape Character

Charter used to escape fist value within a collection, if the value contains operator value.

**Example**
- `["==", 1, 1]` # interpreted as EQ expression
- `["\==", 1, 1]` # interpreted as a collection

> **Default escape character:**
> `\`

### Simplify Options

Options applied while an expression is being simplified.

**Usage**

```py
from illogical.illogical import Illogical
from illogical.parser.parse import Options

ignored_paths = ["ignored"]
ignored_path_rx = [r"^prefix"]

illogical = Illogical(Options(ignored_paths=ignored_paths, ignored_path_rx=ignored_path_rx))
```

#### Ignored Paths

Reference paths which should be ignored while simplification is applied. Must be an exact match.

#### Ignored Paths RegEx

Reference paths which should be ignored while simplification is applied. Matching regular expression patterns.

### Operator Mapping

Mapping of the operators. The key is unique operator key, and the value is the key used to represent the given operator in the raw expression.

**Usage**

```py
from illogical.illogical import Illogical
from illogical.parser.parse import Options, DEFAULT_OPERATOR_MAPPING, EQ

operator_mapping = DEFAULT_OPERATOR_MAPPING.copy()
operator_mapping[EQ] = "IS"

illogical = Illogical(Options(operator_mapping=operator_mapping))
```

**Default operator mapping:**

```py
DEFAULT_OPERATOR_MAPPING = {
    # Logical
    AND:     "AND",
    OR:      "OR",
    NOR:     "NOR",
    XOR:     "XOR",
    NOT:     "NOT",
    # Comparison
    EQ:      "==",
    NE:      "!=",
    GT:      ">",
    GE:      ">=",
    LT:      "<",
    LE:      "<=",
    NONE:     "NONE",
    PRESENT: "PRESENT",
    IN:      "IN",
    NIN:     "NOT IN",
    OVERLAP: "OVERLAP",
    PREFIX:  "PREFIX",
    SUFFIX:  "SUFFIX",
}
```

---

## Contributing

See [contributing.md](https://github.com/spaceavocado/pyillogical/blob/master/contributing.md).

## License

Illogical is released under the MIT license. See [license.md](https://github.com/spaceavocado/pyillogical/blob/master/LICENSE.md).
