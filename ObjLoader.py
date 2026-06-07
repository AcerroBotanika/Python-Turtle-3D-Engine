with open('untitled.obj', 'r') as plik:
    punkty=[]
    linie=[]
    sciany=[]
    pomocnicza=[]
    for wiersz in plik: 
        wiersz=wiersz.strip()
        if wiersz.startswith('v '):
            wiersz=wiersz.split()
            punkty.append([float(wiersz[1]),float(wiersz[2]),float(wiersz[3]),1])
        elif wiersz.startswith('l '):
            wiersz=wiersz.split()
            linie.append([int(wiersz[1])-1,int(wiersz[2])-1])
        elif wiersz.startswith('f '):
            wiersz=wiersz.split()
            pomocnicza=[]
            for i in wiersz:
                
                if i.startswith('f'):
                    continue
                else:
                    i=i.split('/')
                    pomocnicza.append(int(i[0])-1)
            sciany.append(pomocnicza)

print("Punkty:",punkty)
print("Linie:",linie)
print("Sciany:",sciany)