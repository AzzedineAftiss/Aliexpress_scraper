# Aliexpress Scraper 📦

A cool scrapy spider that is used to scrap the data about products from aliexpress and store that data to firebase database!

- Scrap the product data (price, title, nbr of reviews, nbr of orders, product description)
- store the scraped data in firebase database
- Scheduled to run periodically at the end of the every weeks.
- Deployed and scheduled periodically on Heroku for free.

## Steps to deploy to Heroku

- Install the Heroku CLI.
- heroku login
- heroku create
- heroku git:remote -a <HEROKU_APP_NAME>
- git add .
- git commit -am "make it better"
- git push heroku master

Now that the deployment is done, you can test the spider with this command:
- heroku run scrapy crawl aliexpress_scraper.


But in order for the spider to run periodically, you just need to use this command :
- heroku ps:scale clock=1

## Technologies are used :

Aliexpressed uses a manylibraries to work properly:

- [Scrapy] 
- [Selenuim] 
- [Firebase_admin] 
- [Heroku CLI] 
-

## Installation

- Clone this project
- Enter to the project folder
- pip install -r requirements.txt





## License

MIT

