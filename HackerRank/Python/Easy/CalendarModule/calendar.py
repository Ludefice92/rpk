# Enter your code here. Read input from STDIN. Print output to STDOUT
import calendar

m, d, y = input().split()
if m[0] == '0': m = m[-1:]
if d[0] == '0': d = d[-1:]
print(calendar.day_name[calendar.weekday(int(y),int(m),int(d))].upper())
