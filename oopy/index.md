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

## Add a vector and a tuple in either order {: #oopy-radd}

Create a `Vector(1, 2)` and add it to `(3, 4)` — and also add `(3, 4)` to the vector.
Do both additions work?

[% inc radd.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is defining `__add__` but not `__radd__`. When Python evaluates
`vector + (3, 4)`, it calls `vector.__add__((3, 4))`, which works. But for
`(3, 4) + vector`, the left operand is a tuple with no idea how to add a `Vector`.
Python then tries the vector's reflected method `__radd__`, which is not defined, so
it raises `TypeError`.

Shows: that binary operators are not automatically commutative for user-defined types,
and that `__radd__` (reflected add) handles the case where the custom object is on the
right-hand side.

To find it: the traceback says `TypeError: unsupported operand type(s) for +: 'tuple'
and 'Vector'`. Add a `__radd__` method (often implemented by delegating to `__add__`).

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

## Copy an object with nested data {: #oopy-shallowcopy}

Create a `Playlist` with a list of songs, make a copy with `copy.copy`, and add a song
to the copy. Does the original's song list stay unchanged?

[% inc shallowcopy.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is using `copy.copy`, which performs a shallow copy. The new `Playlist` is a
different object, but its `songs` attribute still points to the *same* list object as
the original. Appending to the copy's list therefore mutates the original's list too.

Shows: the difference between shallow copy (`copy.copy`, copies the container but
shares nested objects) and deep copy (`copy.deepcopy`, recursively copies nested
objects).

To find it: print `id(original.songs)` and `id(clone.songs)`. They are the same
number, proving both point to one list. Replace `copy.copy` with `copy.deepcopy` to
copy the list too.

</details>

## Use a custom context manager {: #oopy-contextmanager}

Use a `Timer` inside a `with` block and then call `elapsed()` on the bound variable.
Does it work?

[% inc contextmanager.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `__enter__` never returns `self`. The value returned by `__enter__`
is what the `as` target in `with Timer() as t` binds to. With no `return` statement,
`__enter__` returns `None`, so `t` is `None` and calling `t.elapsed()` raises
`AttributeError`.

Shows: the context-manager protocol, and that `__enter__` must return the resource
(usually `self`) that the `as` clause should bind.

To find it: print `t` inside the `with` block — it will be `None`. Add `return self`
at the end of `__enter__`.

</details>

## Instantiate a class with an abstract method {: #oopy-abstractmethod}

Create a `Dog` from an `Animal` base class that declares an abstract `speak` method.
Does `Dog("Rex")` succeed?

[% inc abstractmethod.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `Dog` does not implement the abstract method `speak`. A class
inheriting from `ABC` with an `@abstractmethod` cannot be instantiated until every
abstract method is implemented in a concrete subclass. Because `Dog` leaves `speak`
unimplemented, `Dog("Rex")` raises
`TypeError: Can't instantiate abstract class Dog with abstract method speak`.

Shows: how abstract base classes enforce a contract, and that a subclass must
implement every abstract method before it can be instantiated.

To find it: the traceback names the abstract method and the class. Add a `speak`
method to `Dog` that returns the appropriate sound.

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

## Check whether a collection is empty {: #oopy-truthiness}

Create an empty `Cart` and test it with `if cart:`. Does Python treat it as empty or
as having items?

[% inc truthiness.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `__len__` always returns 1. Python's truthiness protocol calls
`__bool__` if defined, otherwise `__len__`, and an object is falsy only if `__len__`
returns 0. Because this `__len__` returns 1 even for an empty cart, `if cart:` is
always true.

Shows: Python's truthiness protocol (`__bool__`, then `__len__`), and why a custom
container's emptiness check depends on those methods returning the real size.

To find it: print `len(cart)` — it prints 1 even though the cart is empty. Change
`__len__` to return `len(self._items)`.

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

## Track items added to each account {: #oopy-sharemut}

Create two `BankAccount` objects, add transactions to each, and print each account's
history. Does each account show only its own transactions?

[% inc sharemut.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is that `history = []` is defined at class level, so all instances share the
same list object instead of each having their own, and every account's transactions
appear in every other account.

Shows: the difference between shared mutable class attributes and per-instance
attributes initialized in `__init__`.

To find it: create two accounts, add one transaction to the first and a different one
to the second, then print `alice.history` and `bob.history`. If both lists contain
both transactions, confirm the sharing with `print(BankAccount.history is
alice.history)` — it will print `True`.

</details>

## Initialize a subclass with its parent's attributes {: #oopy-super}

Create a `Dog` named `"Rex"` and call `speak()`. Does it print a sentence with both
the name and the sound?

[% inc super.py scrub="\s*# BUG.*" %]

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The bug is forgetting `super().__init__()`, so the parent's `__init__` is never
called and required attributes are missing when a subclass method tries to use them.

Shows: Python's method resolution order and how to use `super()` correctly.

To find it: instantiate the subclass and immediately try to access a parent-defined
attribute. The `AttributeError` names the missing attribute. Search the subclass
`__init__` for a call to `super().__init__()` — its absence is the cause.

</details>
