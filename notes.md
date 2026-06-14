# Python Engineering Notes

## Table of Contents
- [Object-Oriented Programming](#object-oriented-programming)
  - [The `pass` statement](#the-pass-statement)
  - [Consistent state management in methods](#consistent-state-management-in-methods)
- [Dictionaries](#dictionaries)
  - [Iterating over a dictionary](#iterating-over-a-dictionary)

---

## Object-Oriented Programming

Python is an object-oriented language in which a *class* serves as a blueprint for objects that bundle data (attributes) and behaviour (methods) together. A class is defined with the `class` keyword, and its constructor is the special method `__init__`, which is called automatically whenever a new instance is created.

```python
class RiskMeasures:
    def __init__(self, samples, alpha):
        self.samples = samples
        self.alpha   = alpha
        self.evar    = 0.0
```

Here `self` refers to the instance being constructed. Every method receives `self` as its first argument so that it can read and modify the instance's own attributes.

### The `pass` statement

`pass` is a syntactic no-op: it tells Python "there is nothing to do here." Python requires every indented block to contain at least one statement, so `pass` exists purely to satisfy that requirement when a block would otherwise be empty.

It is **necessary** when writing a class or function whose body has not been implemented yet:

```python
class NotYetImplemented:
    pass          # required: class body cannot be empty

def placeholder():
    pass          # required: function body cannot be empty
```

It is also required when you intentionally want to suppress an exception without taking any action:

```python
try:
    result = 1 / x
except ZeroDivisionError:
    pass          # required: except block cannot be empty
```

It is **useless** (and misleading) as soon as any real code exists in the block. A `pass` that follows a `return` statement is unreachable, because the function has already exited:

```python
def CVaR(self):
    self.var  = np.percentile(self.samples, 100 * self.alpha)
    C         = self.samples[self.samples >= self.var]
    self.cvar = np.mean(C)
    return self.cvar
    pass          # never reached; remove this
```

Similarly, a `pass` inside `__init__` after real assignments does nothing and should be removed. The rule of thumb: use `pass` only when the block has *nothing else* in it. The moment you write any real statement, `pass` becomes noise.

### Consistent state management in methods

When a class stores computed values as instance attributes, every method that produces such a value should update the corresponding attribute before returning it. This keeps the object's state consistent and allows other methods to rely on it without recomputing. In the `RiskMeasures` class, `EVaR` both sets `self.evar` and returns the value, so that either usage pattern works correctly:

```python
def EVaR(self):
    def f(z, alp, s):
        c       = z * np.max(s)
        log_mgf = c + np.log(np.mean(np.exp(z * s - c)))
        return (1 / z) * (log_mgf - np.log(1 - alp))

    res       = minimize_scalar(f, bounds=(1e-6, 100),
                                method='bounded',
                                args=(self.alpha, self.samples))
    self.evar = res.fun
    return res.fun
```

---

## Dictionaries

A dictionary maps keys to values. Keys are typically strings or integers; values can be anything, including numpy arrays.

```python
distributions = {
    'Gaussian':  np.random.normal(0, 1, 1000),
    'Log-normal': np.random.lognormal(0, 1, 1000),
}
```

### Iterating over a dictionary

Looping over a dictionary directly gives you only the **keys**:

```python
for i in distributions:
    print(i)          # prints 'Gaussian', 'Log-normal', ...
    print(i.value)    # AttributeError — i is a string, not an object with .value
```

To get both the key and the value simultaneously, use `.items()`, which returns each entry as a `(key, value)` pair:

```python
for name, samples in distributions.items():
    print(name)       # 'Gaussian', 'Log-normal', ...
    print(samples)    # the numpy array
```

You can also get only values with `.values()`, or only keys with `.keys()`:

```python
for samples in distributions.values():   # values only
    ...

for name in distributions.keys():        # keys only (same as plain loop)
    ...
```

In practice, `.items()` is the most common pattern when you need both — as when looping over distributions and using the name as a plot title.

### `enumerate` — loop with an index

When you need both a counter and the values from an iterable, use `enumerate` instead of maintaining a manual counter variable:

```python
# fragile: i resets or increments in the wrong place
i = 0
for name, samples in distributions.items():
    ...
    i += 1

# clean: enumerate gives (index, value) pairs automatically
for i, (name, samples) in enumerate(distributions.items()):
    ...
```

`enumerate` starts counting from 0 by default. You can change the start: `enumerate(items, start=1)`.

---

## Matplotlib subplots

`plt.subplots(2, 2)` creates a 2×2 grid of axes and returns them as a 2D NumPy array of shape `(2, 2)`. Indexing it directly with a single integer (`ax[0]`) returns a whole row, not a single subplot. To index subplots with a flat counter, call `.flatten()` first:

```python
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
axes = ax.flatten()   # shape (4,) — now axes[0] ... axes[3] work

for i, (name, samples) in enumerate(distributions.items()):
    axes[i].plot(alpha_range, hist_c, label='CVaR')
    axes[i].plot(alpha_range, hist_e, label='EVaR')
    axes[i].set_title(f'{name}')
    axes[i].set_xlabel('Alpha')
    axes[i].set_ylabel('Risk Measure')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()   # prevents subplot titles/labels from overlapping
plt.show()
```

Note that with subplots, labels and titles are set on each axis object (`axes[i].set_xlabel(...)`) rather than on the figure level (`plt.xlabel(...)`).
