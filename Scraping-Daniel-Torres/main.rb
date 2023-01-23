require 'open-uri' # consultar a la plataforma
require 'nokogiri' # formatear, parsear a html
require 'csv' # escribir y leer csv


link = 'https://store.steampowered.com/search/?filter=topsellers&ignore_preferences=1'

CSV.open('steamGames.csv', 'wb') do |csv|
  csv << %w[Nombre Precio Fecha Lenguajes Desarrollador Generos Rating Link]
end

steamHTML = open(link)
datos = steamHTML.read
parsed_content = Nokogiri::HTML(datos)

lista_juegos = parsed_content.css("div#search_resultsRows > a.search_result_row")

puts lista_juegos.length

lista_juegos.each do |game|
  link_game = game['href']
  puts link_game
  
  title = game.css(".title").inner_text
  price = game.css('.search_price').inner_text.strip
  search_released = game.css('.search_released').inner_text
  rating = ""
   
  score_text = game.css('div.search_reviewscore > span').at(0)
  if !(score_text.nil?)
    rating = score_text['data-tooltip-html'].split("<br>", 2).at(1).split("%", 2).at(0)
  end

  parsed_game = Nokogiri::HTML(URI.open(link_game).read)
  
  languages = ""
  count = 0
  parsed_game.css('table.game_language_options tr').each do |val|
    if count > 0
      languages += val.css('td').at(0).inner_text().split().at(0)+";"
    end
    count+=1
  end
  
  languages = languages[0..-2]
  if languages.length() == 0
    languages = ""
  end
  
  developers = ""
  parsed_game.css('#developers_list > a').each do |dev|
    developers += dev.inner_text()+";"
  end
  developers = developers[0..-2]
  if developers.length() == 0
    developers = ""
  end
  
  generos = ""
  parsed_game.css('#genresAndManufacturer > span > a').each do |gen|
    generos += gen.inner_text()+";"
  end
  generos = generos[0..-2]
  if generos.length() == 0
    generos = ""
  end

  puts "Título: #{title}"
  puts "Precio: #{price}"
  puts "Fecha: #{search_released}"
  puts "Lenguajes: #{languages}"
  puts "Desarrollador: #{developers}"
  puts "Generos: #{generos}"
  puts "Rating: #{rating}"
  puts "---"

  CSV.open('steamGames.csv', 'a') do |csv|
    csv << [title, price, search_released, languages, developers, generos, rating, link]
  end
end
