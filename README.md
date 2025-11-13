# IR_Project
Information Retrieval - IKEA hacks 

Theodor Vavassori, Francesc Jordi Sacco

1. HOW TO RUN SPIDERS

# Run IKEA spider
scrapy crawl ikea -o data/ikea_hacks.json

# Run Tosize spider
scrapy crawl tosize -o data/tosize_hacks.json

# Run Reddit spider
scrapy crawl reddit -o data/reddit_hacks.json

# To get single JSON
scrapy crawl ikea -o data/all_hacks.json
scrapy crawl tosize -o data/all_hacks.json
scrapy crawl reddit -o data/all_hacks.json