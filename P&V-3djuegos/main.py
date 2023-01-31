import pandas as pd
import matplotlib.pyplot as plt
import re

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

#¿Cuántos juegos fueron lanzados por año (en orden descendente)?
def games_per_year(df):

    year_dict = dict()

    for index, row in df.iterrows():

        result = re.search(r'\b\d{4}\b', row['lanzamiento'])
        if result:
            year = result.group()
            if year in year_dict:
                year_dict[year] +=1
            else:
                year_dict[year] = 1
    
    # print(year_dict)
    sorted_dict = sorted(year_dict.items(), key=lambda x: x[1], reverse=True)
    year_dict = dict(sorted_dict)
    labels = list(year_dict.keys())
    values = list(year_dict.values())
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()

#¿Cuál es el promedio en rating por año de lanzamiento (en orden descendente)?
def mean_rating_year(df):

    rating_year = dict()

    for index, row in df.iterrows():
        result = re.search(r'\b\d{4}\b', row['lanzamiento'])
        if result:
            year = result.group()
            if year in rating_year:
                rating_year[year][0]+=row['valoracion']
                rating_year[year][1]+=1
            else:
                rating_year[year] = [row['valoracion'],1]
    
    # print(rating_year)
    mean_numbers = list(rating_year.values());
    every_mean = list()
    for el in mean_numbers:
        mean = el[0]/el[1]
        every_mean.append(round(mean,2))

    # labels = list(rating_year.keys())
    rating_year = dict(zip(rating_year.keys(),every_mean));
    sorted_dict = sorted(rating_year.items(), key=lambda x: x[1], reverse=True)
    rating_year = dict(sorted_dict)
    print(rating_year)
    labels = list(rating_year.keys())
    values = list(rating_year.values())
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()

#¿Cuántos juegos se lanzaron por mes en el año 2012?
def twenty_twelve_games(df):

    quanti_dict = dict()
    months_es = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio','julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for index, row in df.iterrows():
        if "2012" in row["lanzamiento"]:
            for month in months_es:
                if month in row["lanzamiento"]:
                    # print("The index of the matching month is:", index)
                    if month in quanti_dict:
                        quanti_dict[month] += 1
                    else:
                        quanti_dict[month] = 1
                    break
    
    labels = list(quanti_dict.keys())
    values = list(quanti_dict.values())
    plt.bar(labels,values, color='green')
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))

    # plt.title("")
    plt.show()

#¿Cuántos juegos, del género de Acción, se lanzaron por mes en el año 2016? 
def twenty_sixteen_action_games(df):

    quanti_dict = dict()
    months_es = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio','julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for index, row in df.iterrows():

        if("Acción" in row["generos"] and "2016" in row["lanzamiento"]):
            for month in months_es:
                if month in row["lanzamiento"]:
                    # print("The index of the matching month is:", index)
                    if month in quanti_dict:
                        quanti_dict[month] += 1
                    else:
                        quanti_dict[month] = 1
    
    sorted_dict = sorted(quanti_dict.items(), key=lambda x: x[1], reverse=True)
    quanti_dict = dict(sorted_dict)
    labels = list(quanti_dict.keys())
    values = list(quanti_dict.values())
    plt.bar(labels,values, color='yellow')
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))

    # plt.title("")
    plt.show()           

#¿Cuáles son los 5 juegos mejor puntuados del 2023?
def twenty_three_top_five(df):
    df = df.sort_values("valoracion",ascending=False)
    values = list()
    labels = list()
    count = 0

    for index, row in df.iterrows():

        if "2023" in row["lanzamiento"]:

            if count == 5:
                break

            labels.append(row["nombre"])
            values.append(row["valoracion"])
            count += 1
    
    print(labels)
    print(values)
    plt.bar(labels,values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()
            

#¿Cuántos juegos tienen el español, el japonés o el inglés como idioma en cualquier forma, ya sea en voces o texto?
def jap_spa(df):

    lang_dict = dict()
    lang_dict['Spanish'] = 0
    lang_dict['English'] = 0
    lang_dict['Japanese'] = 0

    for index, row in df.iterrows():

        if("español" in row["idioma"]):
            lang_dict['Spanish'] += 1
        elif("japonés" in row["idioma"]):
            lang_dict['Japanese'] += 1
        elif("inglés" in row["idioma"]):
            lang_dict['English'] += 1
    
    labels = list(lang_dict.keys())
    values = list(lang_dict.values())
    plt.bar(labels,values, color='orange')
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()

#¿Cuáles son los 5 juegos mejor puntuados con idioma japones incluido?
def top_five_jap(df):
    df = df.sort_values("valoracion",ascending=False)
    values = list()
    labels = list()
    count = 0

    for index, row in df.iterrows():
        
        if("japonés" in row["idioma"]):

            if count == 5:
                break

            labels.append(row["nombre"])
            values.append(row["valoracion"])
            count += 1

    print(labels)
    print(values)
    plt.bar(labels,values, color= 'orange')
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 0.5, str(v))
    plt.show()


#9 funciones para las 9 preguntas

# quanti_val(df)  
# top_ten(df)
# games_per_year(df)
# mean_rating_year(df)
# twenty_twelve_games(df)
# twenty_sixteen_action_games(df)
# twenty_three_top_five(df)
# jap_spa(df)
# top_five_jap(df)