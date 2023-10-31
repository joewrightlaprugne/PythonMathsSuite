# Python Maths Suite
Multi-platform graphing calculator app using the PyGame library. Also includes symbolic differentiation and an equation solver.
## Graphing
Users can plot one or more equations in the form y = f(x), and view their intersections and axis intercepts.

**Planned features:** zooming, parametric graphs in the form (x(t), y(t))
## Differentiation
Users can enter a function in the form y = f(x) and the program will produce an expression for the derivative f'(x). There is also the option to plot the derivative once it has been calculated.

**Planned features:** improved simplification of the output expression
## Equation solver
The program is capable of solving equations in one variable on a given interval (a, b). The solutions to the equation are displayed in a message box.

The program can also solve complex equations in one variable z, where a < Re(z) < b and c < Im(z) < d. The solutions are displayed in a message box and plotted on an Argand diagram (click on the points to reveal their exact values).

**Planned features:** Ability to display complex roots in polar form
## Credits
The evaluate() function in shared.py is a modified version of [ast_calculator by mrfuxi](https://github.com/mrfuxi/ast_calculator), released under the MIT license.
