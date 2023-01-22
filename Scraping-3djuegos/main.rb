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
                row = strip_name  +";"+ link
                csv << row.split(";")
            end
            page += 1 
        end
    end
end

def game_details_csv()
    CSV.open('Scraping-3djuegos/csv/detalles_juegos.csv', 'wb') do |csv|
        columnas = [ "También para:", "Desarrollador:", "Género:", "Jugadores:", "Idioma:","Lanzamiento:" ]
        first_row = "nombre;plataformas-adicionales;desarrollador;generos;jugadores;idioma;lanzamiento;valoracion"
        csv << first_row.split(";")
        lineas = CSV.open('Scraping-3djuegos/csv/juegos.csv', 'rb').readlines()
        juegos = lineas[1...-1]
        juego = 0

        juegos.each do |game|
            link = game[-1]

            begin
                gameHTML = URI.open(link)
                datos = gameHTML.read
                parsed_content = Nokogiri::HTML(datos)
                name = game[0]
                if(game[1].length() < 30)
                    name = game[0]+game[1]
                end
                game_details_line = "".force_encoding("UTF-8")
                val_name = "#{name};".force_encoding("UTF-8")
                game_details_line += val_name
                atributos = []
                values_count = 0

                parsed_content.css(".vat").css(".w100_480").css('.mar_l0_480').css(".a_n").css("dl").each do  |dl|
                    count = 0
                    legal_count = 0
                    legal_indexes = []

                    dl.css("dt").each do  |dt|
                        if (columnas.include?(dt.inner_text))
                            legal_indexes.push(legal_count)
                            values_count += 1
                        end
                        legal_count+=1
                    end

                    dl.css("dd").each do  |dd|
                        value = dd.inner_text.force_encoding("UTF-8")
                        if(legal_indexes.include?(count))
                            game_details_line += "#{value};"
                        end
                        count +=1
                    end
                end

                if (values_count == 6)
                    valoracion = parsed_content.css('#expectativas').css('.s20').inner_text
                
                    if (valoracion.length() < 2)
                        valoracion = "0,0" 
                    end
                    
                    game_details_line += "#{valoracion};"

                    csv << game_details_line.split(";")
                end

            rescue OpenURI::HTTPError => e
                if e.io.status[0] == "404" || e.io.status[0] == "410"
                    puts "Pagina no disponible: #{link}"
                else
                    raise e
                end
            end
        end
    end
end


# games_csv();
game_details_csv();