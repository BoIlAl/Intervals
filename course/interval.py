import numpy as np

BASE_TYPE = (int, float, np.int_, np.float_)

class Interval:
    def __init__(self, left, right):
        if not isinstance(left, BASE_TYPE) and isinstance(right, BASE_TYPE):
            raise ValueError("incorrect data")
        
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right

    @property
    def wid(self):
        return abs(self._right - self._left)

    @property
    def mid(self):
        return (self._left + self._right) * 0.5

    def __add__(self, other):
        if isinstance(other, BASE_TYPE):
            return Interval(left=self._left + other, right=self._right + other)
        
        return Interval(left=self._left + other._left, right=self._right + other._right)

    def __sub__(self, other):
        if isinstance(other, BASE_TYPE):
            return Interval(left=self._left - other, right=self._right - other)
        
        return Interval(left=self._left - other._left, right=self._right - other._right)
    
    def __radd__(self, other):
        if isinstance(other, BASE_TYPE):
            return Interval(left=self._left + other, right=self._right + other)
        
        return Interval(left=self._left + other._left, right=self._right + other._right)

    def __rsub__(self, other):
        if isinstance(other, BASE_TYPE):
            return Interval(left=other - self._left, right=other - self._right)
        
        return Interval(left=other._left - self._left, right=other._right - self._right)
    
    def __mul__(self, other):
        if other > 0:
            return Interval(left=self._left * other, right=self._right * other)
        else:
            return Interval(left=self._right * other, right=self._left * other)
    
    def __rmul__(self, other):  
        if other > 0:
            return Interval(left=self._left * other, right=self._right * other)
        else:
            return Interval(left=self._right * other, right=self._left * other)
    
    def __str__(self):
        return f"[{round(self.left, 5)}, {round(self.right, 5)}]"