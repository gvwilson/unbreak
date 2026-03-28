# Object-Oriented Python

Object-oriented Python looks straightforward until it doesn't work.
A handful of rules govern how Python handles attributes, inheritance, and special methods,
and breaking any one of them silently produces wrong results or a confusing error.
Run each example and read the traceback before looking at the explanation.

## Define a method on a class {: #oopy-no-self}

Create a `Rectangle` with width 4 and height 6 and call `area()`.
Does it return 24?

[% inc no_self.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `self` parameter in `area`. When you call `r.area()`, Python
automatically passes the instance `r` as the first positional argument. A method
without `self` declares zero parameters, so Python sees one argument for zero
parameters and raises `TypeError: area() takes 0 positional arguments but 1 was given`.

Shows: that every instance method must declare `self` as its first parameter so Python
has somewhere to put the instance it passes automatically.

To find it: the traceback says the error is in the call `r.area()` and mentions "0
positional arguments but 1 was given". Change `def area():` to `def area(self):`.

</details>

## Get a value back from a method {: #oopy-no-parens}

Create a `Greeter` and print the result of calling `greet`.
Does the output say `"Hello, world!"`?

[% inc no_parens.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing parentheses. `g.greet` without `()` evaluates to the bound
method object itself—a callable—rather than calling it and returning its string. The
`print` then shows something like `<bound method Greeter.greet of ...>`, which is
the text representation of the method, not the greeting.

Shows: that methods, like all callables, must be called with `()` to run and produce
a return value.

To find it: the output will contain the word `bound method` instead of `Hello`.
Change `g.greet` to `g.greet()`.

</details>

## Make `__init__` set up an object {: #oopy-init-return}

Create a `Config` object and print its `debug` attribute.
Does it print `True`?

[% inc init_return.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `return self` inside `__init__`. Python's object creation protocol
requires `__init__` to return `None`. Any other return value raises `TypeError:
__init__() should return None (not 'Config')`. The object is created before
`__init__` runs, so there is no need to return it—`Config(True)` already produces
the new instance.

Shows: the contract for `__init__`: it initializes an already-created object and
must not return anything.

To find it: the traceback says `TypeError: __init__() should return None`. Remove
the `return self` line.

</details>

## Spell an attribute name consistently {: #oopy-typo-attr}

Create a `Student` and call `greet()`. Does it print the student's name?

[% inc typo_attr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is a typo: `self.nane = name` in `__init__` stores the value under the
misspelled key `nane`. When `greet` reads `self.name`, Python looks for the correctly
spelled attribute, finds nothing, and raises `AttributeError`. Python treats each
spelling as a distinct attribute and never connects them.

Shows: how attribute-name typos produce `AttributeError` at the point of reading, not
at the point of writing, which can make the bug appear to be in the wrong place.

To find it: print `vars(s)` after creating the student. The dictionary will contain
`nane` but not `name`. Fix the spelling in `__init__`.

</details>

## Access the computed area of a circle {: #oopy-prop-call}

Create a `Circle` with radius 5 and print its area. Does it print a number close to 78.5?

[% inc prop_call.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the parentheses in `c.area()`. Because `area` is decorated with
`@property`, accessing `c.area` already calls the function and returns the computed
float. Appending `()` then tries to call that float as if it were a function, raising
`TypeError: 'float' object is not callable`.

Shows: that `@property` turns a method into an attribute-style access—you read it
like data, not call it like a function.

To find it: the traceback says `TypeError: 'float' object is not callable`, pointing
to the line with `c.area()`. Remove the parentheses: `c.area`.

</details>

## Retrieve the top item from a stack {: #oopy-no-return}

Push 42 onto a `Stack` and peek at the top. Does `peek()` return 42?

[% inc no_return.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `return` statement. `peek` computes the top item and assigns
it to `top`, but never returns it. Python then falls off the end of the function and
implicitly returns `None`. Adding 1 to `None` raises `TypeError: unsupported operand
type(s) for +: 'NoneType' and 'int'`.

Shows: that forgetting `return` is silent—no error at the call site—and the failure
only appears when the caller tries to use the `None` value it received.

To find it: print `result` before trying to add 1. It will print `None`. Add
`return top` inside the `if` block.

</details>

## Check whether a status matches a target {: #oopy-is-equals}

Create a `Status("ok")` and call `is_ok()`. Does it return `True`?

[% inc is_equals.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `is` to compare objects. `is` tests whether two names refer to the
exact same object in memory—identity, not equality. `Status("ok")` inside `is_ok`
creates a brand-new object, which is a different object from `self`, so `self is
Status("ok")` is always `False`. The fix is `self.code == "ok"`, which compares
values.

Shows: the difference between `is` (identity) and `==` (equality), and why `is`
should be reserved for comparisons against singletons like `None`, `True`, and `False`.

To find it: print `id(self)` and `id(Status("ok"))` inside `is_ok`. The numbers will
differ. Replace `is` with `==` and compare the `code` attributes directly.

</details>

## Create a person with the right details {: #oopy-wrong-args}

Create a `Person` and call `introduce()`. Does the output contain the correct name and age?

[% inc wrong_args.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the argument order. `Person.__init__` expects `first, last, age`, but the
call passes `"Alice", 30, "Smith"`—putting the age in the `last` position and the
last name in the `age` position. Python has no way to detect the mismatch because all
three arguments are accepted without error, and `introduce` happily uses whatever
values ended up in `self.last` and `self.age`.

Shows: how positional argument order is enforced by position, not by name, and how
using keyword arguments (e.g., `Person(first="Alice", last="Smith", age=30)`) prevents
this class of mistake.

To find it: compare the output of `introduce()` against what you expect. The name and
age will be swapped. Reorder the arguments or switch to keyword arguments.

</details>

## Record a score before reporting it {: #oopy-late-attr}

Create a `Scoreboard` for `"Alice"` and immediately call `report()`.
Does it print a score?

[% inc late_attr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `self.score` is only created inside `record()`, not in `__init__`.
If `report()` is called before `record()` has ever run, `self.score` does not exist
and `report` raises `AttributeError: 'Scoreboard' object has no attribute 'score'`.

Shows: that all instance attributes an object may need should be initialized in
`__init__` so the object is in a consistent state from the moment it is created.

To find it: add `print(vars(board))` after creating the `Scoreboard`. The dictionary
will not contain `score`. Add `self.score = 0` to `__init__`.

</details>

## Show a card as text {: #oopy-repr-none}

Create a `Card` and print its `repr`. Does the output show the rank and suit?

[% inc repr_none.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `return`. The f-string `f"{self.rank} of {self.suit}"` is
evaluated and the resulting string is immediately discarded. `__repr__` then returns
`None` implicitly. Python raises `TypeError: __repr__ returned non-string (type NoneType)`.

Shows: that constructing a value and returning it are two separate steps—building a
string with an f-string does nothing unless the result is returned or assigned.

To find it: the traceback says `TypeError: __repr__ returned non-string`. Add
`return` before the f-string.

</details>

## Store data in an instance {: #oopy-init-attr}

Create a `Point` with `x=3` and `y=4` and call `distance()`.
Does it return 5.0?

[% inc init_attr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `x = x` and `y = y` inside `__init__`. Those lines rebind the local
parameter names to themselves and do nothing else. Without `self.x = x` and
`self.y = y`, the values are discarded the moment `__init__` returns, leaving the
object with no `x` or `y` attribute. Calling `self.x` in `distance` then raises
`AttributeError`.

Shows: that instance attributes must be assigned through `self`, and that a bare
assignment inside a method creates a local variable, not an attribute.

To find it: add `print(vars(p))` after creating the point. The dictionary will be
empty, revealing that no attributes were stored.

</details>

## Build a bag that can hold any items {: #oopy-mutable-default}

Create two `Bag` objects without passing any arguments, add `"apple"` to the first,
and print the second. Is the second bag empty?

[% inc mutable_default.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the mutable default argument `items=[]`. Python evaluates default
argument values once, when the `def` statement runs, not on each call. Every `Bag`
created without an explicit list receives a reference to the same list object. Adding
to one bag therefore adds to all of them.

Shows: why mutable objects (lists, dicts, sets) must never be used as default
argument values, and the standard fix of using `None` as the default and creating a
new list inside the function body.

To find it: print `id(a.items)` and `id(b.items)`. They are the same number,
proving both bags point to one list. Fix it with `def __init__(self, items=None)`
and `self.items = items if items is not None else []`.

</details>

## Track students enrolled in a course {: #oopy-class-var}

Create two `Roster` objects, enroll `"Alice"` in the math roster, and print the
science roster's students. Is the science list empty?

[% inc class_var.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `students = []` at class level. That makes `students` a class variable:
one list shared by every `Roster` instance. When `enroll` calls
`self.students.append(student)`, Python looks up `self.students`, finds the class
variable, and mutates it in place. The mutation is visible through every instance.

Shows: the difference between a class variable (one copy, shared) and an instance
variable (one copy per object), and why mutable class variables are a common source
of unexpected sharing.

To find it: print `Roster.students` after enrolling Alice. It already contains her
name, confirming the class-level list was modified. Fix it by moving the list into
`__init__`: `self.students = []`.

</details>

## Extend a class with a new attribute {: #oopy-super-init}

Create a `Dog` named `"Rex"` with breed `"Labrador"` and call `describe()`.
Does it print a sentence with both pieces of information?

[% inc super_init.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `super().__init__(name)` call inside `Dog.__init__`. Python
does not automatically run the parent class's `__init__`. Without that call,
`Animal.__init__` never runs, so `self.name` is never set. `describe` then raises
`AttributeError` when it tries to read `self.name`.

Shows: that subclass `__init__` methods must explicitly call the parent's `__init__`
to initialize inherited attributes, and that forgetting this call produces an error
only when the missing attribute is accessed, not at construction time.

To find it: add `print(vars(d))` right after creating the dog. The dictionary will
contain `breed` but not `name`. Add `super().__init__(name)` as the first line of
`Dog.__init__`.

</details>

## Display an object as a string {: #oopy-str-type}

Create a `Temperature` of 100 degrees and print it.
Does the output look like a sensible string?

[% inc str_type.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is returning `self.celsius` (an integer) from `__str__`. Python requires
`__str__` to return a `str` object. When it gets anything else, it raises
`TypeError: __str__ returned non-string`. The value is never printed.

Shows: that special methods must return the exact type Python expects, and that
returning the wrong type produces a `TypeError` that mentions the method by name.

To find it: the traceback says `TypeError: __str__ returned non-string (type int)`.
Fix it by returning `str(self.celsius)` or `f"{self.celsius} C"`.

</details>

## Count how many widgets exist {: #oopy-static-class}

Create two `Widget` objects and call `Widget.how_many()`.
Does it return 2?

[% inc static_class.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `@staticmethod`. A static method receives no implicit first argument, so
`cls` is undefined inside `how_many` and raises `NameError`. The fix is `@classmethod`,
which passes the class itself as the first argument, conventionally named `cls`.

Shows: the distinction between `@staticmethod` (no implicit arguments) and
`@classmethod` (receives the class as `cls`), and when each decorator is appropriate.

To find it: the traceback says `NameError: name 'cls' is not defined`. Replace
`@staticmethod` with `@classmethod` and add `cls` as the first parameter of
`how_many`.

</details>

## Update the radius of a circle {: #oopy-property-setter}

Create a `Circle` with radius 5, update the radius to 10, and print the area.
Does the area reflect the new radius?

[% inc property_setter.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `radius` is a read-only property. A `@property` decorator with no
corresponding `@radius.setter` creates a getter only. Assigning `c.radius = 10`
raises `AttributeError: can't set attribute` before `area()` is ever reached.

Shows: that a `@property` alone is read-only, and that a companion setter must be
defined explicitly for assignments to work.

To find it: the traceback pinpoints the assignment line. Add a setter:

```python
@radius.setter
def radius(self, value):
    self._radius = value
```

</details>

## Accept any animal in a function {: #oopy-isinstance-check}

Call `make_sound` with a `Dog` object.
Does it print `"Woof"`, or does it raise an error?

[% inc isinstance_check.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `type(creature) == Animal`. The `type()` function returns the exact runtime
type of an object. A `Dog` instance has type `Dog`, not `Animal`, so the comparison is
`False` and the function raises `ValueError`—even though `Dog` is a subclass of `Animal`.
`isinstance(creature, Animal)` returns `True` for any instance of `Animal` or any of
its subclasses.

Shows: that `type()` checks for an exact match while `isinstance()` respects the
inheritance hierarchy, and that `isinstance` is almost always the right choice.

To find it: print `type(d)` and `type(d) == Animal` before calling the function. The
output `False` makes the bug obvious. Replace `type(creature) == Animal` with
`isinstance(creature, Animal)`.

</details>

## Read a private attribute from outside a class {: #oopy-name-mangling}

Create a `BankAccount`, deposit some money, and print the balance by accessing
`account.__balance` directly. Does it print the correct total?

[% inc name_mangling.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is accessing `account.__balance` from outside the class. Python rewrites any
identifier starting with two underscores (but not ending with two) to
`_ClassName__attribute` at compile time. Inside the class, `self.__balance` is
automatically translated to `self._BankAccount__balance`. Outside the class, writing
`account.__balance` is not translated, so Python looks for a literal attribute named
`__balance`, finds nothing, and raises `AttributeError`.

Shows: Python's name-mangling mechanism for double-underscore attributes and how to
access them from outside if necessary.

To find it: print `dir(account)` and look for `_BankAccount__balance` in the output.
Use the public `get_balance()` method instead, or access the mangled name directly
as `account._BankAccount__balance` for debugging.

</details>

## Use points as dictionary keys {: #oopy-eq-hash}

Create two equal `Point` objects and check whether the second is in a set containing
the first. Does `p2 in seen` return `True`?

[% inc eq_hash.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is defining `__eq__` without also defining `__hash__`. Python's data model
specifies that any class defining `__eq__` must also define `__hash__`, or Python
sets `__hash__ = None` automatically. An object with `__hash__ = None` is unhashable:
it cannot be placed in a `set` or used as a `dict` key, raising `TypeError: unhashable
type: 'Point'`.

Shows: the connection between `__eq__` and `__hash__`, and why both must be defined
together when value equality is needed.

To find it: the traceback mentions `TypeError: unhashable type`. Add a `__hash__`
method that returns a hash based on the same fields used in `__eq__`:

```python
def __hash__(self):
    return hash((self.x, self.y))
```

</details>

## Iterate over a countdown twice {: #oopy-iterator-reuse}

Create a `Countdown` from 3 and iterate over it twice.
Do both passes produce `[3, 2, 1]`?

[% inc iterator_reuse.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that the `Countdown` object is both an iterable and its own iterator.
`__iter__` returns `self`, so the second call to `list(c)` reuses the same object,
which still has `self.current == 0` from the first pass. `__next__` immediately
raises `StopIteration`, producing an empty list.

Shows: the iterator protocol and the difference between an iterable (has `__iter__`
returning an iterator) and an iterator (has `__next__`). A reusable iterable should
return a fresh iterator object from `__iter__`, not `self`.

To find it: print `c.current` between the two calls. It will be 0. Fix it by
extracting the iteration state into a separate class:

```python
def __iter__(self):
    return CountdownIterator(self.start)
```

</details>

## Build a query with method chaining {: #oopy-method-chain}

Build a `QueryBuilder`, chain `.filter()` and `.limit()`, and call `.build()`.
Does it return a dictionary with both values?

[% inc method_chain.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the missing `return self` in `filter`. Every method in a fluent interface
must return the object it was called on so the next method has something to call.
Without `return self`, `filter` returns `None`. Calling `.limit(10)` on `None` raises
`AttributeError: 'NoneType' object has no attribute 'limit'`.

Shows: how method chaining works and the discipline required to make every step
return `self`.

To find it: the traceback says the error is on the chained line, pointing at `.limit`.
The call before it—`filter`—is the culprit. Add `return self` at the end of `filter`.

</details>

## Add a prefix to log messages {: #oopy-attr-shadow}

Create an `AppLogger` and call `run()`.
Does it print a log message, or does it raise an error?

[% inc attr_shadow.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is `self.log = "application"` inside `__init__`. That statement creates an
instance attribute named `log` that holds the string `"application"`. When Python
later looks up `self.log` in `run()`, it finds the instance attribute first and
ignores the inherited `log()` method. Calling the string with `self.log("Starting up")`
raises `TypeError: 'str' object is not callable`.

Shows: how instance attributes shadow methods of the same name, and why attribute
names must not collide with method names inherited from parent classes.

To find it: print `type(self.log)` inside `run()` before the call. It will show
`<class 'str'>`. Rename the attribute—for example, `self.prefix = "application"`—and
update any references to it.

</details>

## Get the number of items in a dataset {: #oopy-len-type}

Create a `DataSet` with three numbers and call `len()` on it.
Does it return the integer 3?

[% inc len_type.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is the `/` operator in `__len__`. In Python 3, `/` always performs true
(floating-point) division and always returns a `float`, even when both operands are
integers and the result is a whole number. `len()` requires an integer return value
and raises `TypeError: 'float' object cannot be interpreted as an integer` when it
gets a float.

Shows: the difference between `/` (true division, returns float) and `//` (integer
division, returns int), and that `__len__` has a strict return-type contract.

To find it: the traceback says `TypeError` and names `__len__`. Replace `/` with
`//`, or just write `return len(self.data)`.

</details>

## Add a third coordinate to a point {: #oopy-slots-attr}

Create a `Point` with `x=3` and `y=4`, add `z=0`, and print all three coordinates.
Does it work?

[% inc slots_attr.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `__slots__` lists only `x` and `y`. When `__slots__` is defined,
Python removes the instance `__dict__` and allows only the named attributes. Assigning
`p.z = 0` raises `AttributeError: 'Point' object has no attribute 'z'` because `z`
is not in the slot list.

Shows: what `__slots__` does (restricts attributes, saves memory, improves attribute
access speed) and the trade-off it imposes (no dynamic attributes unless `__dict__`
is also included in `__slots__`).

To find it: the traceback points directly at `p.z = 0`. Either add `"z"` to
`__slots__`, or remove `__slots__` entirely if dynamic attributes are needed.

</details>
