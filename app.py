import re
from flask import Flask, request, render_template
import detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form():
    link = request.form['link']
    try:
        output = detector.stats(link)
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="static/styles/styles.css">
        </head>
        <body>
            <br><br><br><br><br>
            Out of the """ + str(output[1]) + """ songs that they have in all their playlists, """ + str(output[0]) + """ of them were from BTS. <br>

            That means <h1>""" + str(output[2]) + """%</h1> of their playlists are BTS.

            <br></br><a href="/">back</a>
        </html>
        """
    except:
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="static/styles/styles.css">
        </head>
        <body>
            <h1>Invalid ID</h1>

            <a href="/">back</a>
        </html>
        """