import re

regexes = [
    # bug number
    'bug[# \t]*[0-9]+',
    'pr[# \t]*[0-9]+',
    'show\_bug\.cgi\?id=[0-9]+',
    '\[[0-9]+\]',
    # plain number
    '[0-9]+',
    # keyword
    'fix(e[ds])?|bugs?|defects?|patch',
]

s = "Fixed bug 53784"
r = 'bug[# \t]*[0-9]+'

s1 = "52264, 51529"
r1 = '[0-9]+'

s2 = "Updated copyrights to 2004"

x = re.search(r1, s1)
print(x)