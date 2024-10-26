mcesre
======

## Movement

Similar to Turtle Graphics these commands move a cursor through the cartesian plane:

    >       Right
    v       Down
    <       Left
    ^       Up


## Drawing

    l       Draw lines between any preceeding movements
    s       Combines 3 movements to form a spline
    L       Draw a line between the previous position and the current position
    M       Duplicate last point in the path, preventing next `L` instruction from drawing anything.

### Lines

    >l      Draw a horizontal line
    >vl     Draw a line going from the starting point to the right and then down, forming a top-right corner
    >v<^l   Draw a square

### Splines

TBD


## Transformations

Transformations apply to any subsequent movements until the context is reset


### Scaling

    2x      Scale x axis by 2
    2x3     Scale x axis by 2/3 (0.6666...)
    1.5y    Scale y axis by 1.5
    3y2     Scale y axis by 1.5
    1e-3z   Scale bot axes by 0.001
    1z2     Scale bot axes by 0.5

Examples:

    2x>l            Draw a horizontal line of length 2
    2x;3y >v<^l     Draw a square of with 2 and height 3

### Rotation

    0.5r    Rotate 180° counterclockwise
    1r3     Rotate 120° counterclockwise


Examples:

    1r3 >l 1r3 >l 1r3 >l        Draw a triangle
    1r4>l 1r4>l 1r4>l 1r4>l     Draw a diamond shape

### Shearing

TBD


## Context manipulation

### Isolated context (...)

The transformation matrix and current position are reset at the end of the context.

    (       Create a new context, keeping the current position and applied transformations.
    )       Close context


Examples:

    (>l)(vl)(<l)(^l)        Draw a "+" sign

In the example above after each line is drawn, `()` will restore the cursor position to what it was before


    (3z >v<^l) >v >v<^l     Draw a square with side of length 1 inside a square with side of length 3

### Combining context [...]

The transformation matrix is reset at the end of the context but the position is preserved and any movements are combined.

    [       Create a new context, keeping the current position and applied transformations.
    ]       Close context


Examples:

    [>v]l       Combine `>v` to draw a diagonal line going down
    [2x>]v>^l   Draw a dipper


### Resetting transformations

    |   Reset tranformations matrix based on enclosing context


**Example:**

    7r8[3x>l | > 2x>l | > >l]       Draw three lines with decreasing length
    7r8(3x>l | > 2x>l | > >l)       Draw three lines with decreasing length

In the example above `|` will reset the scaling `x` transformations but not the rotation `r`.



## Functions

    =       Declare a function
    !       Call a function
    $       Reference to a function or function argument

> Note:
>
> Function declarations need to come at the end of the program, after an 'un-opened' `]` or `)` otherwise they will get executed as normal code.


> Note 2:
>
> Only the first statement is considered as part of the function. To use multiple statements, place them inside `()` or `[]`.


**Example:**

Define a function `$func` that takes `0` arguments and draws a horizontal line:

    $func!          Call `$func` with no arguments
    ]               Terminate the program
    0$func=>l       Implementation of `$func`. The instruction `]` prevents this from being executed


Define a function `$func` that takes `2` arguments and uses them to draw a rectangle, the first argument being used as the width and the second as the height:

    3,6$func!                   Call `$func` with `3` as the first argument and `6` as the second
    ]                           Terminate program
    2$func=[$1x $2y >v<^l]      `$1` will load the value `3` and `$2` will load the value 6


## Conditional statements

    ?       Skip next statement if the condition is `0`
    b       Jump to the end of the current context


Examples:


    0?>l vl         Draw a vertical line
    1?>l vl         Draw a horizontal line followed by a vertical line
    [0?>lb vl]      Draw a vertical line
    [1?>lb vl]      Draw a horizontal line and jump to end of context `]`


## Loop

    :       Repeat statement

Examples:

    4:[> >l]        Draw 4 spaced horizontal lines
    3:1r3>l         Draw a triangle
    4:1r4>l         Draw a square
    4:1r4(>l)       Draw a "+" sign


## Arithmetic instructions

    +       Addition
    -       Subtraction
    *       Multiplication
    /       Division


> Note:
>
> Arithmetic instructions have no precedence and associate left.

