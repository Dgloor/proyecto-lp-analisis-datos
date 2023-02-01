import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_csv("P&V-Daniel Torres\steamGames.csv",
                 names=["Nombre", "Precio", "Fecha", "Lenguajes", "Desarrollador", "Generos", "Rating", "Link"],
                 header=0)


for index, row in df.iterrows():
    row["Rating"] = pd.to_numeric(row["Rating"]);


#¿Cuántos juegos tienen una valoración mayor al 50% y una valoración menor al 50%?
def pregunta1(df):
    higher = 0
    lower = 0

    for index, row in df.iterrows():
        if row["Rating"] >= 50:
            higher += 1
        else:
            lower += 1
    
    print("Mayores a 50%: {}".format(higher))
    print("Menores a 50%: {}".format(lower))

    labels = ['Mayor a 50%', 'Menor a 50%']
    values = [higher, lower]

    plt.barh(labels, values)
    
    for i, v in enumerate(values):
        plt.text(v, i, str(v),va='center', ha='left')

    plt.show()


#¿Cuáles son los 10 juegos mejor puntuados del género de Supervivencia/Accion?
def pregunta2(df):
    df = df.sort_values("Rating",ascending=False)
    values = list()
    labels = list()
    count = 0
    for index, row in df.iterrows():
        
        if count == 10:
            break
        
        genre = str(row["Generos"])
        if genre != "nan":
            print("genero")
            print(genre)

            if genre.lower().find("action"):                
                labels.append(row["Nombre"])
                values.append(row["Rating"])
                count += 1
    
    print(labels)
    print(values)
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()


#¿Cuántos juegos fueron lanzados por año (en orden descendente)?
def pregunta3(df):

    year_dict = dict()

    for index, row in df.iterrows():

        print('fecha')
        print(row['Fecha'])

        result = re.search(r'\d{4}', row['Fecha'])
        if result:

            year = result.group()

            if year in year_dict.keys():
                year_dict[year] +=1
            else:
                year_dict[year] = 1

    print(year_dict)
    
    sorted_dict = sorted(year_dict.items(), key=lambda x: x[1], reverse=True)
    year_dict = dict(sorted_dict)

    labels = list(year_dict.keys())
    values = list(year_dict.values())

    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()



# 3 funciones para las preguntas 1, 2, y 3 repectivamente segun la reparticion de preguntas.

# pregunta1(df) 
# pregunta2(df)
# pregunta3(df)

