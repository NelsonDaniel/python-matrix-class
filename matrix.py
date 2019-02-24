import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vector1, vector2):
    """
    Returns the dot product between two vectors. It can be
    used as a helper function to calculate the multiplication
    by two matrices.
    """
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]

    return result

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise ValueError("Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise NotImplementedError("Calculating determinant not implemented for matrices larger than 2x2.")
        
        return self.g[0][0] * self.g[1][1] - self.g[0][1] * self.g[1][0]

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise ValueError("Cannot calculate the trace of a non-square matrix.")
        result = 0
        for i in range(self.h):
            for j in range(self.w):
                if i == j:
                    result += self.g[i][j]
        return result

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        inverse = []
        if not self.is_square():
            raise ValueError("Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise NotImplementedError ("inversion not implemented for matrices larger than 2x2.")

        if self.h == 1:
            inverse.append([1/self.g[0][0]])
        elif self.h == 2:
            if self.determinant() == 0:
                raise ValueError("Cannot find the inverse of a matrix that has a determinant value of 0")
            else:
                a = self.g[0][0]
                b = self.g[0][1]
                c = self.g[1][0]
                d = self.g[1][1]
                coefficient = 1 / (a * d - b * c)
                inverse = [
                    [d, -b],
                    [-c, a]
                ]

                for i in range(self.h):
                    for j in range(self.w):
                        inverse[i][j] = inverse[i][j] * coefficient
        return Matrix(inverse)


    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        result = zeroes(self.w, self.h)
        for i in range(self.h):
            for j in range(self.w):
                result[j][i] = self.g[i][j]
        return result

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise ValueError("Matrices can only be added if the dimensions are the same") 
        
        result = zeroes(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                result[i][j] = self.g[i][j] + other[i][j] 
        
        return result


    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg = zeroes(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                neg[i][j] = - self.g[i][j]
        
        return neg

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise ValueError("Matrices can only be added if the dimensions are the same") 

        result = zeroes(self.h, self.w)
        for i in range(self.h):
            for j in range(self.w):
                result[i][j] = self.g[i][j] - other[i][j] 
        
        return result

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if self.w != other.h:
            raise ValueError("Matrix multiplication is only possible if the width of the first matrix is the same as the height of the second matrix") 

        result = zeroes(self.h, other.w)
        for i in range(self.h):
            for j in range(other.w):
                result[i][j] = dot_product(self.get_row(i), other.get_column(j))

        return result
        
    def get_row(self, row_number):
        return self.g[row_number]

    def get_column(self, column_number):
        result = []
        for i in range(self.h):
            result.append(self.g[i][column_number])

        return result

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        result = Matrix(self.g)
        if isinstance(other, numbers.Number):           
           for i in range(self.h):
               for j in range(self.w):
                   result[i][j] = result[i][j] * other
        
        return result
            