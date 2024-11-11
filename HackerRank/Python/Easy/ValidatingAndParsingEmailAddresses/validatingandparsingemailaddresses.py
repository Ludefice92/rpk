# Enter your code here. Read input from STDIN. Print output to STDOUT
import email.utils
import re
n = int(input())
regex = r'^[a-zA-Z][\w\.-]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$'

for _ in range(n):
    name, email_addr = email.utils.parseaddr(input())
    
    if re.match(regex, email_addr):
        print(email.utils.formataddr((name, email_addr)))
