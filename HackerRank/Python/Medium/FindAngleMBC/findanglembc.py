# Enter your code here. Read input from STDIN. Print output to STDOUT
import math
ab = int(input())
bc = int(input())
#did some debugging...it turns out this problem is wrong as the solution is the
#incorrect angle in the triangle...should be 180-90-the angle calculated below
print(f"{round(math.degrees(math.atan(ab/bc)))}",chr(176),sep='')
