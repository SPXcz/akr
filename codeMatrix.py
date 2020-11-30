"""
File stegano.py byl vytvoren ze ucelem ulozeni zpravy, koncoveho znaku a hashe do
matice v dec tvaru

Funkce:
  messageTohash(message) - funkce pro hashovani zpravy
  messageToBinary(message) - funkce, ktera prevadi zpravu do binarniho kodu
  lsbMetrixMessage(imageName, text) - nejdulezitejsi funkce, funkce pomoci metodz LSB meni posledni
    bit cisla v binarnim podle zpravy v binarnim kouu. 
  lsbMatrixHash(imageName, text) - Do matice se od konce uklada hash v binarnim tvaru stejne jako v predchozim tvaru. 
    Hash slouzik overeni zda bylo s daty nejak nakladano. Je to bezpecnostni prvek
  export(imgName) - funkce, ktera zavola nejdulezitejsi funkce v programu

    IMPORT -> napr 'import codeMatrix as cM
    pristup k funkcim -> cM.lsbMetrixMessage()
"""
try:
  import numpy as np
  import hashlib
  import codePNG as cP
except Exception as e:
    print("'codeMatrix.py' EXCEPTION modul: {}".format(e))

"""
  Input: string - zprava kterou zada uzivatel
  Output: string - return zahashovana data v binarnim tvaru

  Funkce, ktera na zaklade vstupniho testu vraci zhashovany text pomoci sha256
"""
def messageToHash(message):
  try:
    hashMessage = hashlib.sha256(message.encode('utf-8')).hexdigest()
    return messageToBinary(hashMessage)
  except(ValueError, TypeError):
    print("Value or Type error occurred")

"""
  Input: string - zprava ktera ma byt prevedena do binarniho kodu
  Output: string - zprava v binarnim kodu

  Pomocna funkce, ktera slouzi k prevadeni stringu do binarniho tvaru
"""

def messageToBinary(message):
  try:
    if (len(message) == 0):
      print("Zadna data")
    else:
      return ''.join([format(ord(i), "08b") for i in message]) #vratim zpravu v binarnim kodu
  except(TypeError, ValueError):
    print("Value or Type error occurred")
  
"""
Input: imgName, text
Output: matrixData, text, total_items - pomocna promena pro prochazeni matice, pomocna promena pro prochazeni matice
text, pocet polozek v matici do kterych se daji ukladat data

Hlavni funkce tohoto filu, ktera pomoci metody LSB meni posledni byt matice v binarnim tvaru
na konec zpravy je zasifrovan koncovy znak 00000011, ktery slouzi k signalizci konce textu
pri desteganografii. Od konce matice je opet pomoci metody LSB ukladan binarni kod
zhasovane vstupni zpravy. Ulozeny hash ma bezpecnostni prvek, pomoci ktereho se bude v dalsich
funkci overovat zda nebyla data nejak upravovana

Matice ma tvar bud [[255,255,255,255], [255,255,255,255]] nebo [[255,255,255], [255,255,255]]
"""

def lsbMetrixMessage(imgName, text):
  
  matrixData, _= cP.encodeImgFormat(imgName)

  b_message = "00000010" + messageToBinary(text) + "00000011" #ulozim retezec zacatku + zpravu binarnim kodu + ukladam ukoncujici retezec pro UTF8

  total_items = matrixData.size #pocet prvku v matici se kterymi je mozne pracovat
  req_pixels = len(b_message) #pocet potrebnych prvku se urcuje z delky zpravy
  shapeTuple = matrixData.shape #promena, ktera vraci shape matice a nasledne se pouziva pro prochazeni matice
  shapeTuple = shapeTuple + (0,) #pridavam nulu

  index = 0

  for p in range(total_items): 
    for q in range(shapeTuple[2],shapeTuple[1]):
      if (index < req_pixels):
          matrixData[p][q] = int(bin(matrixData[p][q])[2:-1] + b_message[index],2)
          index +=1
          """
          Binarni kod kazdeho znaku ma 0b100, pomoci slicingu odstranim 0b a posledni znak
          misto posledni znaku dosadim znak zhasovane zpravy v binarnim kodu. Nasledne to prevedeme zpet do dec
          """

  return shapeTuple, matrixData, text, total_items

"""
input : imgName, text

Funcke, ktera od konce matice opet pomoci metody LSB uklada zhasovany text. Text zde ukladame jako bezpecnosti prvek abych zjistili,
zda nebylo s obrazkem nejak nakladano. Funkce je podobna jako predchozi s tim rozdilem, ze v ni pracujeme s obracenou matici. 

"""
def lsbMetrixHash(imgName, text):
  shapeTuple, matrixData, text, total_items = lsbMetrixMessage(imgName, text)

  b_hash_message = messageToHash(text) #puvodni zhasovana zprava v binarnim kodu
  req_pixels = len(b_hash_message) #pocet potrebnych prvnku se urcuje z delky hashe
  matrixData = np.flip(matrixData) #otacim matici z [[64,64,64,1], [255,255,255,1]] do [[1,255,255,255], [1,64,64,1]]
  
  index = 0

  for p in range(total_items): 
    for q in range(shapeTuple[2],shapeTuple[1]):
      if (index < req_pixels):
          matrixData[p][q] = int(bin(matrixData[p][q])[2:-1] + b_hash_message[index],2)
          index +=1
          """
          Binarni kod kazdeho znaku ma 0b100, pomoci slicingu odstranim 0b a posledni znak
          misto posledni znaku dosadim znak zhasovane zpravy v binarnim kodu. Nasledne to prevedeme zpet do dec
          """
  matrixData = np.flip(matrixData) #otocim matici zpet
  cP.matrixToImg(imgName, matrixData)


"""
input: imgName, text

Pomocna funkce, ktera vyvolava ulozeni zpravy a hashe do obrazku
"""

def export(imgName, text):
  text = cP.checkInputText(text, cP.getMaxSizeText(imgName))
  lsbMetrixHash(imgName, text)
