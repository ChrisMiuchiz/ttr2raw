import struct
import sys

def stripquotes(s):
    out = s
    if ((s.startswith('"') and s.endswith('"')) or
        (s.startswith("'") and s.endswith("'"))):
        out = s[1:-1]
    return out
        
def main():
    if len(sys.argv) != 3:
        print('USAGE: %s <Input .ttr file> <Output .raw file>' % sys.argv[0].split('\\')[-1])
        return

    infile = stripquotes(sys.argv[1])
    outfile = stripquotes(sys.argv[2])
    
    with open(infile, 'rb') as file:
        data = file.read()

    sizeX = 0x201
    sizeY = 0x201
    start = 0x18C
    raw = b''
    for y in range(0, sizeY*4, 4):
        for x in reversed(range(0, sizeX*4, 4)):
            #.ttr files store heights as signed, short, big endian, integers.
            #.ttr files also seem to store some texture tiling data.
            #That data is ignored.
            height = struct.unpack('>h', data[start + x + (y*sizeX) :
                                             start + x + (y*sizeX) + 2])[0]
            
            #Shift the heights halfway up the integer space, since
            #.RAW files are unsigned. This will make terrain at height 0
            #end up at height 0x8000 (decimal 32768)
            height += 0x8000

            #Convert to unsigned, short, little endian, integers.
            height = struct.pack('H', height)

            #Append it to one big string of binary data
            raw += height
            
    with open(outfile, 'wb') as file:
        file.write(raw)

if __name__ == '__main__':
    main()
