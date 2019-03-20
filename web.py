from web_scraper import Scraper
from flask import Flask, render_template, request
from wtforms import Form


class Config:
    """ Application configuration"""
    DEBUG = False
    TESTING = False
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '7d441f27d441f27567d441f2b6176a'  # random hex string


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Home page to scraping web pages
    """
    if request.method == 'POST':
        url = request.form['url']
        scraper = Scraper(url)

        return render_template('home.html', form=Form, data=scraper.result)

    return render_template('home.html', form=Form, data=None)


if __name__ == "__main__":
    app.run()
