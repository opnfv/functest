import tarfile

print 'creating archive'
out = tarfile.open('tarfile_add.tar', mode='w')
try:
    print 'adding README.txt'
    out.add('README.txt')
finally:
    print 'closing'
    out.close()

print
print 'Contents:'
t = tarfile.open('tarfile_add.tar', 'r')
for member_info in t.getmembers():
    print member_info.name