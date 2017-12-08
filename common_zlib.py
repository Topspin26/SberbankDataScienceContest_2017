import zlib
import os

def from_zlib(filename):
    if not os.path.exists(filename) and os.path.exists(filename + '.zlib'):
        with open(filename + '.zlib', 'rb') as myfile:
            zs = myfile.read()
        s = zlib.decompress(zs).decode('utf-8')
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(s.replace('\r\n', '\n'))

def to_zlib(filename):
    if not os.path.exists(filename + '.zlib'):
        with open(filename, encoding='utf-8') as fin:
            s = fin.read()
        zs = zlib.compress(s.encode('utf-8'))
        with open(filename + '.zlib', 'wb') as fout:
            fout.write(zs)

def rm_zlib(filename):
    if os.path.exists(filename + '.zlib'):
        os.remove(filename + '.zlib')
