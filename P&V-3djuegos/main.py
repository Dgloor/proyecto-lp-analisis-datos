import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("detalles_juegos.csv", 
                 names=["nombre", "plataformas-adicionales", "desarrollador", "generos", "jugadores", "idioma", "lanzamiento", "valoracion"],
                 header=0)



for index, row in df.iterrows():
    row["valoracion"] = pd.to_numeric(row["valoracion"].replace(",", "."));


#¿Cuántos juegos tienen una valoración mayor a 5 y una valoración menor a 5?
def quanti_val(df):
    higher_five = 0
    lower_five = 0

    for index, row in df.iterrows():
        if row["valoracion"] >= 5:
            higher_five += 1
        else:
            lower_five+= 1
    
    print(str(higher_five)+' - '+str(lower_five))

    labels = ['Mayor a 5', 'Menor a 5']
    values = [higher_five, lower_five]
    plt.barh(labels,values)
    for i, v in enumerate(values):
        plt.text(v, i, str(v),va='center', ha='left')
    plt.show()



#¿Cuáles son los 10 juegos mejor puntuados del género de Supervivencia?
def top_ten(df):
    df = df.sort_values("valoracion",ascending=False)
    values = list()
    labels = list()
    count = 0
    for index, row in df.iterrows():
        
        if count == 10:
            break
        
        genre = str(row["generos"])

        if not genre.lower().find("supervivencia") == -1:
            labels.append(row["nombre"])
            values.append(row["valoracion"])
            count += 1
    
    print(labels)
    print(values)
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()

# ¿Cuál es la plataforma más presente en el listado de juegos?
def plat_quanti(df):

    plats = dict()

    platforms = [("xbox series", "xseries"),
            ("xbox one", "xone"), 
            ("nintendo switch", "nswitch")]

    for index, row in df.iterrows():
        raw_plat = str.lower(row["plataformas-adicionales"])
        if raw_plat.find(',') == -1:
            plat = raw_plat
            for x in platforms:
                if plat == x[0]:
                    plat = x[1]
                    break
            if plat in plats:
                plats[plat] += 1
            else:
                plats[plat] = 1
        else:
            plat_div = raw_plat.split(',')
            for cad in plat_div:
                plat = cad.strip()
                for x in platforms:
                    if plat == x[0]:
                        plat = x[1]
                        break
                if plat in plats:
                    plats[plat] += 1
                else:
                    plats[plat] = 1

    labels = list(plats.keys())
    values = list(plats.values())
    print(plats)
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()

# quanti_val(df)
# plat_quanti(df)
top_ten(df)