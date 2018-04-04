
################################################################################
## Demonstration program for class Date
################################################################################

import date

A = date.Date( 1, 1, 2014 )

print( A )
print( A.to_iso() )
print( A.to_mdy() )
print( A.is_valid() )
print()

B = date.Date( 12, 31, 2014 )

print( B )
print( B.to_iso() )
print( B.to_mdy() )
print( B.is_valid() )
print()

C = date.Date()

C.from_iso( "2014-07-04" )

print( C )
print( C.to_iso() )
print( C.to_mdy() )
print( C.is_valid() )
print()

D = date.Date()

D.from_mdy( "March 15, 2015" )

print( D )
print( D.to_iso() )
print( D.to_mdy() )
print( D.is_valid() )
print()

E = date.Date()

print( E )
print( E.to_iso() )
print( E.to_mdy() )
print( E.is_valid() )
print()


# Added for lab11a

# Erroneous arguments
F = date.Date(13, 40, 2017)
# From ISO w/ spaces
G = date.Date()
G.from_iso("2017 12 31")
# From MDY with spaces
H = date.Date()
H.from_mdy("December 31, 2018")
# Erroneous arguments for MDY and ISO
I = date.Date()
I.from_iso("this is not a date")

I = date.Date()
I.from_mdy("this is not a date")

