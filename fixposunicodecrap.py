# If the leading bit is 0, it's a single-byte character (ASCII).
# If the leading bits are 110, it's a two-byte character.
# If the leading bits are 1110, it's a three-byte character.
# If the leading bits are 11110, it's a four-byte character.
# motherfuckers making nme do this again jesus fucking
# christ leave my shit alone !!!!
stupidteststr = "Oh pretty sure there was an executive order 🙄"

#F0 9F 99 84
# oh and apparently i can't go to a fucking doctors appointment without 
# risk of having either shoot the fucking doctor on a repeat visit 
# or without having some jackass replace me .
# fucking hell.



twobyte = 192 #110
threebyte = 224
fourbyte =  240 

def countUnicodeChars(s):
    b = bytes(s, 'utf-8')
    spos = []
    skip = 0

    for i in range(0, len(b)):

        if skip > 0: 
            skip = skip -1
            continue

        if b[i] & fourbyte == fourbyte:
            spos.append((i,4, b[i:i+4])) 
            skip  = 3
            continue

        if b[i] & threebyte == threebyte:
            spos.append((i,3, b[i:i+3]))
            skip = 2 
            continue
            
        if b[i] & twobyte == twobyte:
            spos.append((i,2, b[i:i+2]))
            skip = 1 
            continue

   
    # print (len(s))
    # print (s)
    # print (len(b))
    # print (b)

    sum = 0 

    for p in spos:
        sum = sum + p[1]
    #     print(p)

    # print(len(b) - sum  + len(spos))

    
    return {'chars':spos, 
            'countunicodechar': len(spos),
            'unicodebytecount': sum,  
            'lengthbytestring':len(b), 
            'asoneperunicodelen' :len(b)-sum+len(spos),
             'lenoriginal': len(s) }


# #length is supposedly 46
# counts = countUnicodeChars(stupidteststr)

# #length is supposedly 32
# anotherstupidteststr = b'*&^%$#@!\xc3\x83\xc2\xb7\xc3\x83\xc2\xb7=/_<>[]?,;:"\'-)({}|\\`~'.decode('utf-8')

# counts = countUnicodeChars(anotherstupidteststr)
