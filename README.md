# synchronous-model-checking
A simple implementation of model checking in structures consisting of synchronous relations on the set of finite strings.

# What does that mean?
It is a well-known fact that (Peano) arithmetic is [undecidable](https://en.wikipedia.org/wiki/Decidability_(logic)), in the sense that there is no algorithm that can tell us whether a given
first-order statement such as "for all x, there exists a y such that y > x" or "there exists an x such that for all a, b, x = ab implies
a = 1 or b = 1" is true or not, when we interpret the quantifiers as ranging over the natural numbers and the allowed relations/functions
are addition, multiplication, and comparison (less than). This is unfortunate, because decidability is a highly desirable property for
many reasons, the most obvious being the ability to (at least in principle) write and execute a computer program to tell us if a statement
is true or false. So a natural question is: can we sacrifice something in order to get decidability?

The answer is yes. One thing we can sacrifice is the expressiveness of our relations. More precisely, if we require that all our relations
are synchronous (which means they are n-ary relations on the set of finite words that are described by finite state transducers of a
specific type), we obtain decidable structures. Examples of synchronous relations that you will find in the `tests.py` file include:
- Equality
- Prefix (is a word x a prefix of y?)
- Successor (is y = S(x), where all words are interpreted as numbers in reverse binary?)
- Addition (is z = x + y, where all words are interpreted as numbers in reverse binary?)
- Evolution of cellular automata (does x evolve to y in one step, under some given automaton rule?)

We can then ask any first-order-definable question about these relations (more formally, we can write any first-order formula involving
these relations, run the algorithm, and see if the formula is true or false). Some interesting examples of the kinds of questions we
can ask that are included in the `tests.py` file include:
- Are these relations reflexive? Irreflexive? Symmetric? Transitive?
- Are these relations functions?
- If these relations are functions, are they injective? Surjective?
- For fixed k, is there a k-cycle? That is, are there k distinct points x_1, ..., x_k such that x_i is related to x_{i + 1}, for each i?

Of course, these questions only have to do with binary relations, but relations of any arity work, and they can be mixed. For instance,
in `tests.py`, we verify that 1 + 1 = 2, which involves the 2-ary successor relation and the 1-ary "equal to (the constant) 2" relation. 

# How does this work?
This is pretty involved; I'll write a post about it later. Some of the high-level design choices are detailed in `explanation.pdf`, but
they assume familiarity with the basic idea behind the algorithm.

# How do I use it?
Clone the repository and run `python tests.py`. If you would like to define your own relations and/or write your own formula, see `explanation.pdf`
for a rundown of the syntax.
