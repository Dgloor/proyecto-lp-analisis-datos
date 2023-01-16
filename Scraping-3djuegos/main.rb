require 'open-uri'
require 'nokogiri'
require 'csv'
require 'fileutils'

# FileUtils.mkdir_p 'Scraping-3djuegos/csv'

def games_csv()
    CSV.open('Scraping-3djuegos/csv/juegos.csv', 'wb') do |csv|
        csv << %w[Nombre Link]
        page=0
        while (page<100)
            link = "https://www.3djuegos.com/pc/juegos/#{page}/"
            puts "Scrapeando la url #{link}"

            mainHTML = URI.open(link);
            datos = mainHTML.read
            parsed_content = Nokogiri::HTML(datos)
            movie_list_cont = parsed_content.css('.hr_15').css('ul')

            movie_list_cont.css("li").each do |juego|
                puts juego.css(".s18i").inner_text
                puts juego.css(".s18i").attr('href')
                nombre = juego.css(".s18i").css(".col_plat_i").inner_text
                strip_name = nombre.strip()
                link = juego.css(".s18i").css(".col_plat_i").attr('href')
                row = strip_name  +","+ link
                csv << row.split(",")
            end
            page += 1 
        end
    end
end

def game_details_csv()
    CSV.open('Scraping-3djuegos/csv/detalles_juegos.csv', 'wb') do |csv|
        columnas = [ "También para:", "Desarrollador:", "Género:", "Jugadores:", "Idiona:", "Lanzamiento:" ]
        first_row = "nombre;plataformas-adicionale;desarrollador;generos;jugadores;duracion;idioma;lanzamiento"
        csv << first_row.split(";")
        lineas = CSV.open('Scraping-3djuegos/csv/juegos.csv', 'rb').readlines()
        juegos = lineas[1...-1]
        juego = 0
        juegos.each do |game|
            link = game[1]
            gameHTML = URI.open(link)
            datos = gameHTML.read
            parsed_content = Nokogiri::HTML(datos)

            name = game[0]
            game_details_line = "#{name};"
            atributos = []
            
            parsed_content.css(".vat").css(".w100_480").css('.mar_l0_480').css(".a_n").css("dl").each do  |dl|
                count = 0
                legal_count = 0
                legal_indexes = []

                dl.css("dt").each do  |dt|
                    if (columnas.include?(dt.inner_text))
                        legal_indexes.push(legal_count)
                    end
                    legal_count+=1
                end

                dl.css("dd").each do  |dd|
                    value = dd.inner_text
                    if(legal_indexes.include?(count))
                        game_details_line += "#{value};"
                    end
                    count +=1
                end
            end

            csv << game_details_line.split(";")
        end
    end
end

# games_csv();
game_details_csv();