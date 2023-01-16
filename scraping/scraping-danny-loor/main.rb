require 'open-uri'
require 'nokogiri'
require 'csv'

# Scraping Eneba
#CSV.open('games.csv', 'w') do | csv | 
#  csv << %w[titulo ]
#end


URL = 'https://www.eneba.com'

html_data = URI.open(URL + '/latam/store/all')
parsed_data = Nokogiri::HTML(html_data.read)
games_links = parsed_data.css('.oSVLlh')

CSV.open('games.csv', 'a') do | csv | 
  games_links.each do | game_link |
    game_url =  URL + game_link['href']
    game_html_data = URI.open(game_url)
    game_parsed_data = Nokogiri::HTML(game_html_data.read)
    titulo = game_parsed_data.css('.C68dpx').text
    calificacion = game_parsed_data.css('.d52_Iq').text
    lista_plataformas = game_parsed_data.css('.oBo9oN').css('li')
    lista_categorias = game_parsed_data.css('.aoHRvN').css('li')
  
    plataformas = ''

    lista_plataformas.each do | plataforma |
      plataformas += plataforma.text + '|'
    end
    plataformas = plataformas.chop

    categorias = ''

    lista_categorias.each do | categoria |
      categorias += categoria.text + '|'
    end
    categorias = categorias.chop

    csv << [titulo, calificacion, plataformas, categorias]
  end
end
