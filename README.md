# Take-Homes
A collection of take home interview problems and their solutions

1. Problem: Perimeter product

You are given a list of line segments represented as a set of two x,y points.

( ((x1, y1), (x2, y2)),

  ((x3, y3), (x4, y4)), …. )


For an example of a simple square:

( ((1, 1), (1, 2)),

  ((1, 2), (2, 2)),

  ((2, 2), (2, 1)),

  ((2, 1), (1, 1)), )


The final result we wish to calculate is to find the multiplicative product of all perimeters of all the individual enclosed areas.  For the example above, it is straightforward where there is only one enclosed area that has a perimeter of 4.  So the final answer is 4.

For a stranger shape, we draw an hourglass shape:
( ((1, 1), (1, 2)),

  ((1, 2), (2, 1)),

  ((2, 1), (2, 2)),

  ((2, 2), (1, 1)), )

Note: There are two areas, but we do not explicitly write the intersection point at the neck of the hourglass. 

Each individual triangle has a perimeter of ~2.4142 or ( 1+sqrt(2) ), so the product of all perimeters is 5.82842 or (3 + 2 * sqrt(2)).  Note, we expect the floating point solution, not the exact values.  They are there just for illustrative purposes.

For a more complex shape, we draw a window:

( ((1, 1), (1, 2)),

  ((1, 2), (2, 2)),

  ((2, 2), (2, 1)),

  ((2, 1), (1, 1)), 

  ((1.5, 1), (1.5, 2)),

  ((1, 1.5), (2, 1.5)), )


In this example there are 4 areas each with a perimeter of 2.  Making the final answer 16.

Note: We do NOT double count the larger original square, nor the 4 possible rectangles. 

Please submit your code and the solution to our test cases.  You can assume that there are no dangling edges (a line that is not part of an area). 

Please feel free to use the programming language of your choice. 

Please find the multiplicative perimeter product for the following points:

( ((1, 1), (1, 2)),

  ((1, 2), (1.8, 2)),

  ((1.8, 2), (1.8, 1)),

  ((1.8, 1), (1, 1)),

  ((1.2, 1), (1.2, 2)),

  ((1.6, 1), (1.6, 2)),

  ((1, 1.5), (1.6, 1.8)),

  ((1, 1.3), (1.8, 1.7)),

  ((1.2, 1.2), (1.8, 1.5)), )
