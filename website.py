'''
The python source code for the smart alarm clock
'''
from flask import Flask, render_template, redirect, request
import main_scraper
APP = Flask(__name__)

@APP.route('/')
def display_server():
    return render_template("index.html")

if __name__ == "__main__":
    main_scraper.main()
    APP.run(debug=True, use_reloader=False)
