from sys import argv
import codeMatrix as inlsb
import LSBdecode as outlsb
# Hlavní soubor, který slučuje a řídí celkou aplikaci.
# Získává argumenty z terminálu a podle nich řídí chod aplikace.
# 
# Autor: Ondřej Chudáček

try:
    if(argv[1] == "-h" and argv[2] is not None):
        path = argv[2]

        if(argv[3] == "-t"):
            with open(argv[4], "r") as f:
                message = f.read().replace("\n", " ")
        else:
            message = argv[3]
        inlsb.export(path, message)
        print("Your image is in ./data directory")
    elif(argv[1] == "-g" and argv[2] is not None):
        path = argv[2]
        outlsb.export(path)
    elif(argv[1] == "-help"):
        print("Usage: python3 App.py [MODE] [FILE PATH] \"[MESSAGE]\"")
        print("MODE:")
        print("-h\tHide a message into your provided image")
        print("-g\tGet a message from your provided image")
        print("FILE PATH:")
        print("[FILE PATH]\tPath to the file with your picture. File has to end with either .png or .jpg")
        print("MESSAGE:")
        print("[MESSAGE]\tString with your message. Must begin and end with \"")
    else:
        print("Wrong argument. Use -help to explore options.")
except Exception as e:
    print(e)
    print("Use python3 App.py -help to get more info.")

