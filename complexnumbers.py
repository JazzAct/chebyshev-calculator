import cmath

z = 1 + 1j
print(cmath.phase(z))  # Returns the phase (argument) in radians
print(cmath.exp(z))    # Returns e**z

#The content below doesn't need cmath

z1 = 3 + 4j  # Creates a complex number with real part 3 and imaginary part 4
z2 = -2j     # Creates a complex number with real part 0 and imaginary part -2


z3 = complex(5, 6) # Creates a complex number with real part 5 and imaginary part 6
z4 = complex(7)    # Creates a complex number with real part 7 and imaginary part 0 (7+0j)

z = 1 + 2j
print(z.real)  # Output: 1.0
print(z.imag)  # Output: 2.0