from sys import argv
import akr.codeMatrix as inlsb
import akr.LSBdecodePNG as outlsb

try:
    if(argv[0] == "-e"):
        inlsb.export(argv[1])
        print("Your image is in your directory")
    elif(argv[0] == "-d"):
        outlsb.export(argv[1])
    else:
        print("Wrong flag. Chose either \"-d\" for decoding or \"-e\" for encoding")
except Exception as e:
    print(e+" You have to add path to your picture.")