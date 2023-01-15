require 'open-uri'
require 'nokogiri'
require 'csv'
require 'fileutils'

FileUtils.mkdir_p 'Scraping-3djuegos/csv'

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