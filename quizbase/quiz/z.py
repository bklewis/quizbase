vList = [2, 1]
score = 0.0
twos = vList.count(2)
ones = vList.count(1)
zeros = vList.count(0)
print '[%s]' % ', '.join(map(str, vList))
print "Twos", twos
print "Ones", ones
print "Zeros", zeros
score += twos * (1.0 / (2 ** ones)) * (0 ** zeros)
print score
