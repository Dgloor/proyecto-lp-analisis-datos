import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("steamGames.csv", 
                 names=["Nombre", "Precio", "Fecha", "Lenguajes", "Desarrollador", "Generos", "Rating", "Link"],
                 header=0)


for index, row in df.iterrows():
    row["Rating"] = pd.to_numeric(row["Rating"]);


#¿Cuántos juegos tienen una valoración mayor al 50% y una valoración menor al 50%?
def quanti_val(df):
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
