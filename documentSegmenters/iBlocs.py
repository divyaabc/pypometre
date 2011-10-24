#!/usr/bin/env python
# -+- encoding: utf-8 -+-

#fichier= "Tblocs.txt"

def makeHTML(fichier,lesBlocs):
    Fh= open(fichier,"r")
    contenu= ""
    buff= Fh.readline()
    while buff:
        contenu += buff
        buff= Fh.readline()
    Fh.close()
    Fh= open("./out.html",'w')
    Fh.write("<html><head><style>div {border: 1px solid; margin: 3px;}</style></head><body>\n")
    # lesBlocs= [(level,debut,fin)]
    debuts= []
    fins= []
    for b in lesBlocs:
        if b[0] != 0:
            debuts.append(b[1])
            fins.append(b[2])

    offsets= []
    offsets.extend(debuts)
    offsets.extend(fins)
    offsets.reverse()

    i=0
    new= ""
    for c in contenu:
        while i in debuts:
            debuts.remove(i)
            new += "<div><pre>"
        while i in fins:
            fins.remove(i)
            new += "</pre></div>"
        new += c
        i +=1

    new= new.replace("\n","<br/>")

    Fh.write(new)
    Fh.write("</body></html>")

    Fh.close()

    #print "="+contenu[64]+"="
    print contenu.replace("\n","!")
    print (" "*9+"|")*8
    print debuts
    print fins
    print new

def getLevel(ligne):
    indentChars= ['\t',' ']
    level= 0
    while ligne[level] in indentChars :
      level += 1
    return level
#    if ligne[0] in indentChars:
#        indentChar= ligne[0]
#         On compte le nombre
#        level=1
#        while ligne[level] == indentChar:
#            level +=1
#    else:
#        level= 0
#    return level

def trouveBlocs(texteEntree):
    texte= texteEntree.split('\n')
    lesBlocs= []

    # Pour chaque ligne
    numLigne= -1
    stack= []
    offset= 0
    prevLevel= -1
    for buff in texte:
        buff += "\n"
        numLigne +=1
        # On cherche le niveau d'indentation
        level= getLevel(buff)

        # ##Si level=0 -> programme principal -> on continue
        # Idem si c'est la meme indentation
        # Idem si la ligne est vide
        if level == prevLevel or buff.strip()== "":
            # On incremente l'offset
            offset += len(buff)
            continue

        # Si la ligne est + indentee, on entre dans un bloc,
        # on ajoute ce bloc dans la pile avec son niveau
        # son offset et son numero de ligne
        # et on continue
        if level > prevLevel:
            stack.append( (level,offset,numLigne) )

            # On incremente l'offset
            offset += len(buff)
            prevLevel= level
            continue

        # Si l'indentation est moins grande,
        # on depile stack jusqu'a retrouver le bon niveau
        if level < prevLevel:
            while stack[-1][0] > level:
                bloc= stack.pop()
                lesBlocs.append( (bloc[0],bloc[1],offset) )
#                print "bloc (%i): %i - %i" % (bloc[0],bloc[1],offset)
            prevLevel= level

            offset += len(buff)
            continue

    # A la fin on ferme les blocs restant
    while len(stack) > 0:
        bloc= stack.pop()
        lesBlocs.append((bloc[0],bloc[1],offset-1))
#        print "bloc (%i): %i - %i" % (bloc[0],bloc[1],offset-1)

    return lesBlocs
