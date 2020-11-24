try:
    import codeMatrix 
    import inputMenu as iM
except Exception as e:
    print("'main' {}".format(e))

imgFormat, matrixData, imgName = codeMatrix.lsbMetrixHash()
iM.encodeMatrixFormat(imgName, imgFormat, matrixData)
#01101000 01101001
#11111111