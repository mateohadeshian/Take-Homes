import math

################
# ASSUMPTIONS: #
################

# No dangling edges
# No overlapping Co-linear segments
# The perimeter that we care about of an individual enclosed area is its OUTER perimeter:
# '--> If we wanted to include the interior perimeter in the calculus, then after we've found all shapes, we could check each shape to see 
#      if there exists any other shape(s) that are inscribed in it, then add all of the interior shapes' segments to the outer's list of segments. 
#      Note: we'd also need to make sure that the inscribed shapes we've found are not inscribed within a larger inscribed shape that isn't
#            our original.

####################
# Data Structures: #
####################

# Point           : tuple of floats
#                   '--> (float, float)
# segment         : tuple of points
#                   '--> (point, point)
# Adjacency Matrix: dictionary with points as keys and a list of adjacent points as values
#                   '--> {point: [points]}


# the number of decimal places our floats get rounded to after division 
# This keeps inaccurate float math from causing segments to disconnect
decimalPlaces = 6

# takes in a list of segments and returns the sum of their distances as a float.
def getPerimeter(shape: [((float, float), (float, float))]) -> float:
	perimeter = 0
	for segment in shape:
		perimeter += math.sqrt(((segment[0][0] - segment[1][0]) * (segment[0][0] - segment[1][0])) + ((segment[0][1] - segment[1][1]) * (segment[0][1] - segment[1][1])))

	return perimeter

###########################################################################################
# Section Below includes logic for splitting all intersecting segments into smaller parts #
###########################################################################################

# takes in 3 points and returns an int.
# returns the direction of the path that would be taken if they were traversed in order.
# returns 0 if co-linear, 1 if clockwise, 2 if counterclockwise
def getOrientation(p1: (float, float), p2: (float, float), p3: (float, float)) -> int: 
	val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
	if val == 0:
		return 0
	return 1 if (val > 0) else 2; 

# takes in 2 segments and returns a bool.
# returns whether or not 2 segments have exactly one intersection point
# returns False if the segments share an endpoint
def intersects(segment1: ((float, float), (float, float)), segment2: ((float, float), (float, float))) -> bool:

	# returns False if the segments share an endpoint
	for point1 in segment1:
		for point2 in segment2:
			if (point1 == point2):
				return False

	o1 = getOrientation(segment1[0], segment1[1], segment2[0])
	o2 = getOrientation(segment1[0], segment1[1], segment2[1])
	o3 = getOrientation(segment2[0], segment2[1], segment1[0])
	o4 = getOrientation(segment2[0], segment2[1], segment1[1])

	return (o1 != o2 and o3 != o4)


# takes in 2 intersecting segments and returns a point
# returns the instersection point of 2 intersecting segments
# assumes segments intersect 
def getIntersectionPoint(segment1: ((float, float), (float, float)), segment2: ((float, float), (float, float))) -> (float, float):
	
	# segment1 Line represented as a1x + b1y = c1
	a1 = segment1[1][1] - segment1[0][1]
	b1 = segment1[0][0] - segment1[1][0]
	c1 = a1 * (segment1[0][0]) + b1 * (segment1[0][1])
 
	# segment2 Line represented as a2x + b2y = c2
	a2 = segment2[1][1] - segment2[0][1]
	b2 = segment2[0][0] - segment2[1][0]
	c2 = a2 * (segment2[0][0]) + b2 * (segment2[0][1])
 
	determinant = a1 * b2 - a2 * b1

	x = (b2 * c1 - b1 * c2) / determinant
	y = (a1 * c2 - a2 * c1) / determinant

	# round our values to keep segments from disconnecting due to inaccurate float math
	return (round(x, decimalPlaces), round(y, decimalPlaces))

# takes a list of segments returns a list of segments.
# returns a list of segments identical to the input list, but replaces all pairs of
# intersecting segments with their 3- or 4-segment representations
def splitIntersections(segments: [((float, float), (float, float))]) -> [((float, float), (float, float))]:

	# for every pair of segments
	for i in range(len(segments)):
		segment1 = segments[i]

		for segment2 in segments:

			# if they are not the same and intersect,
			# remove the 2 segments and replace with 4 new segments that 
			# meet at the intersection point

			# recurse (for the case where one segmentement is intersected more than once)
			if segment1 != segment2 and intersects(segment1, segment2):

				intersectionPoint = getIntersectionPoint(segment1, segment2)

				# remove intersecting segments
				segments.remove(segment1)
				segments.remove(segment2)

				# Add their 3 or 4 segment replacements
				# '-> make sure no segments of length 0 are added.
				if segment1[0] != intersectionPoint:
					segments.append((segment1[0], intersectionPoint))
				if segment1[1] != intersectionPoint:
					segments.append((segment1[1], intersectionPoint))
				if segment2[0] != intersectionPoint:
					segments.append((segment2[0], intersectionPoint))
				if segment2[1] != intersectionPoint:
					segments.append((segment2[1], intersectionPoint))

				# recursive case. intersection found. 
				# no need to recurse on the segment1s with no intersecting segment2s
				return segments[:i] + splitIntersections(segments[i:])

	# base case. no intersections
	return segments

#########################################
# End of Intersection Splitting Section #
#########################################

# takes in a list of edges and returns an adjacency matrix
def generateAdjacencyMatrix(segments: [((float, float), (float, float))]) -> {(float, float): (float, float)}:

	matrix: {(float, float): [(float, float)]} = {}

	for segment in segments:
		matrix.setdefault(segment[0],[]).append(segment[1])
		matrix.setdefault(segment[1],[]).append(segment[0])

	return matrix

# takes in 2 points and an adjacency matrix. returns a tuple that contains a point and a float.
# finds the next point adjacent to the current (aside from the previous) that requires the 'sharpest right turn'
# returns that point alongside the interior angle between previousPoint, currentPoint, and nextPoint (where currentPoint is the angle)
def rightmostPath(currentPoint: (float, float), previousPoint: (float, float), matrix: {(float, float): [(float, float)]}) -> ((float, float), float):

	rightmostAngle = 0
	rightmost: (float, float) = None

	for nextPoint in matrix[currentPoint]:

		if nextPoint != previousPoint:

			angle = math.atan2(currentPoint[1] - nextPoint[1], currentPoint[0] - nextPoint[0]) - math.atan2(currentPoint[1] - previousPoint[1], currentPoint[0] - previousPoint[0])

			if angle < 0:
				angle += math.pi * 2
				
			if angle < rightmostAngle or rightmostAngle == 0:

				rightmostAngle = angle
				rightmost      = nextPoint

	return (rightmost, rightmostAngle)

# takes a point and a list of segments
# returns whether the point is in any of the segments in the list
def pointInPath(point: (float, float), path: [((float, float), (float, float))]):

	return any(point in segment for segment in path)

# takes in a list of segments and returns a list of lists of segments.
# returns all the individual enclosed areas (no segments going through it) represented as lists of segments
# that comprises their OUTER perimeters.
def findAllShapes(segments: [((float, float), (float, float))]) -> [[(float, float), (float, float)]]:

	segments = splitIntersections(segments)

	matrix = generateAdjacencyMatrix(segments)

	shapes: [[((float, float),(float, float))]] = []

	################################################################################################
	# Since we split all intersections, each directional edge can only be in a maximum of 1 shape  #
	# We can create a memoization table to remove redundant detections                             #
	# Looking up if a non-duplicate key exists in a python dictionary should be constant time      #
	################################################################################################
	segmentsInDocumentedShapes: {((float, float),(float, float)): bool} = {}

	for segment in segments:
		# for each segment, search for shapes clockwise from each point
		for i in range(2):
			if i != 0:
				# reverse segment
				segment = segment[::-1]

			# check if the current directional segment's shape has already been found
			if segment in segmentsInDocumentedShapes:
				continue

			targetPoint     = segment[0]

			currentPoint    = segment[1]
			previousPoint   = segment[0]

			segmentsInPath  = [segment]
			currentAngleSum = 0

			while True:
				
				# iterate the currentPoint, previousPoint, and currentAngleSum
				temp               = currentPoint
				(currentPoint, a)  = rightmostPath(currentPoint, previousPoint, matrix)
				currentAngleSum   += a
				previousPoint      = temp

				# failure base case
				# if current point has already been visited and isn't target,
				# then no shape to be found
				if pointInPath(currentPoint, segmentsInPath) and currentPoint != targetPoint:
					break

				# add the current segment to the path
				segmentsInPath.append((previousPoint, currentPoint))

				# success base case:
				# check if shape found, otherwise iterate
				if currentPoint != targetPoint:
					continue

				# get angle and point information for what might be the last edge
				(nextPoint, angle) = rightmostPath(currentPoint, previousPoint, matrix)		

				# double check that the rightmost path is in fact the very first edge in the shape
				# '--> this is for the inscribed shapes connected at a single point case
				# double check that the interior angles of the shape all sum up to the internal angle formula for polygons
				# '--> this avoids counting the outer perimeter of compound shapes as a shape
				if not (nextPoint == segmentsInPath[0][1] and round(currentAngleSum + angle, decimalPlaces) == round((len(segmentsInPath) - 2) * math.pi, decimalPlaces)):
					continue

				# Shape Found!
				# Note: We don't need to verify that the new shape has not already been found because our memoization table
				#       has the added benefit of removing redundant detections
				shapes.append(segmentsInPath)

				# memoize all directional segments in the shape so that they don't get checked again.
				for segmentInShape in segmentsInPath:
					segmentsInDocumentedShapes[segmentInShape] = True 

				break

	return shapes

# Takes in a list of segments and returns a float.
# Calculates & returns the perimeter product of the provided list of segments.
# Input Assumptions:
# - no dangling edges
# - No overlapping Co-linear segments
def getPerimeterProduct(segments: [((float, float), (float, float))]) -> float:

	if len(segments) < 3:
		return 0

	shapes = findAllShapes(segments)

	perimeterProduct = 1

	for shape in shapes:

		perimeterProduct *= getPerimeter(shape)

	return perimeterProduct

##########
# Tests: #
##########

# Test: Simple Square
segments = [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1))]
assert(getPerimeterProduct(segments) == 4)

# Test: Hourglass
segments = [((1, 1), (1, 2)), ((1, 2), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (1, 1))]
# margin for error +- .001
assert(abs(getPerimeterProduct(segments) - 5.82842) < .00001)

# Test: Window
segments = [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1)),  ((1.5, 1), (1.5, 2)), ((1, 1.5), (2, 1.5))]
assert(getPerimeterProduct(segments) == 16)

# Test: Taller Window (make sure we can handle dividing a segment more than once)
segments = [ ((0, 0), (0, 3)), ((0, 3), (2, 3)), ((2, 3), (2, 0)), ((0, 0), (2, 0)), ((0, 1), (2, 1)), ((0, 2), (2, 2)), ((1, 0), (1, 3)) ]
assert(getPerimeterProduct(segments) == math.pow(4, 6))

# Test: Further divided window with center point that connects to all points (make sure we can handle myriad intersections at one point)
segments = [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1)),  ((1.5, 1), (1.5, 2)), ((1, 1.5), (2, 1.5)), ((1,1), (2,2)), ((1, 2), (2,1))]
assert(round(getPerimeterProduct(segments), decimalPlaces) == round(math.pow(1 + (math.sqrt(2) / 2), 8), decimalPlaces))

# Test  : Inscribed triangles connected at a single point (should detect a hexagon and the smaller triangle)
segments = [((1,1), (1,6)), ((1,6), (6,1)), ((1,1), (6,1)), ((1,1), (2,4)), ((2,4), (4,2)), ((4,2), (1,1))]
assert(round(getPerimeterProduct(segments), decimalPlaces) == 240.028272)

# Test             : Polygon with hole (inscribed squares)
# Expected behavior: produces the product of the outer perimeters of each shape (not including the interior perimeter of the larger square).
segments = [((1, 1), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (2, 1)), ((2, 1), (1, 1)), ((0, 0), (0, 3)), ((0, 3), (3, 3)), ((3, 3), (3, 0)), ((3, 0), (0, 0)) ]
assert(getPerimeterProduct(segments) == 4 * 12)

# Final Test Case
# the perimeter product (calculated by hand) of the list below is 5.571255151316118
segments = [((1, 1), (1, 2)),((1, 2), (1.8, 2)),((1.8, 2), (1.8, 1)),((1.8, 1), (1, 1)),((1.2, 1), (1.2, 2)),((1.6, 1), (1.6, 2)),((1, 1.5), (1.6, 1.8)),((1, 1.3), (1.8, 1.7)),((1.2, 1.2), (1.8, 1.5))]
assert(round(getPerimeterProduct(segments), decimalPlaces) == 5.571255)