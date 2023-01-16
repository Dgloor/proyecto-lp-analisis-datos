require 'open-uri'
require 'nokogiri'
require 'csv'

# Scraping Eneba
URL = 'https://www.eneba.com'
page = 1
n_games = 0

CSV.open('games.csv', 'w') do | csv | 
  csv << %w[titulo calificacion plataformas categorias idiomas fecha_lanzamiento desarrollador]

  while (page < 100)
    page_url = URL + "/latam/store/all?page=#{page}"
    puts "Realizando scraping de: " + page_url
    html_data = URI.open(page_url)
    parsed_data = Nokogiri::HTML(html_data.read)
    games_links = parsed_data.css('.oSVLlh')

    games_links.each do | game_link |
      game_url =  URL + game_link['href']
      game_html_data = URI.open(game_url)
      game_parsed_data = Nokogiri::HTML(game_html_data.read)
      titulo = game_parsed_data.css('.C68dpx').text
      calificacion = game_parsed_data.css('.d52_Iq').text

      # Plataformas
      lista_plataformas = game_parsed_data.css('.oBo9oN').css('li')
      plataformas = ''
      lista_plataformas.each do | plataforma |
        plataformas += plataforma.text + '|'
      end
      plataformas = plataformas.chop

      # Cagegorias
      lista_categorias = game_parsed_data.css('.aoHRvN').css('li')
      categorias = ''
      lista_categorias.each do | categoria |
        categorias += categoria.text + '|'
      end
      categorias = categorias.chop

      # Idiomas
      lista_idiomas = game_parsed_data.css('.r1iAKt').css('li')
      idiomas = ''
      lista_idiomas.each do | idioma |
        idiomas += idioma.css('span').text + '|'
      end
      idiomas = idiomas.chop
  
      fecha_lanzamiento = game_parsed_data.css('.r1iAKt').css('div')[0]
      unless fecha_lanzamiento.nil?
        fecha_lanzamiento = fecha_lanzamiento.text
      end

      desarrollador = game_parsed_data.css('.r1iAKt').css('div')[2]
      unless desarrollador.nil?
        desarrollador = desarrollador.text
      end
  
      csv << [titulo.to_s, calificacion.to_f, plataformas.to_s, categorias.to_s, idiomas.to_s, fecha_lanzamiento.to_s, desarrollador.to_s]
      
      n_games += 1
    end
    
    page += 1
  end
end
