a = 0
b = 10
c = 11
d = "{}{}{}".format(
    str(a) + "d " if a > 0 else "", str(b) + "h " if b > 0 else "", str(c) + "m " if c > 0 else ""
)
print(d)