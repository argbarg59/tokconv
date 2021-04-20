import requests as req
from bs4 import BeautifulSoup as bs
from flask import request
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app)

def ttdowner_get(url):
    #Get source links
    ttdowner_source = "https://ttdownloader.com/"
    ttdowner_api = "https://ttdownloader.com/ajax/"

    #Get token value and auth cookies
    ttdowner_html = req.get(ttdowner_source)
    ttdowner_parsed = bs(ttdowner_html.text, "html.parser")
    token = ttdowner_parsed.find(id="token")['value']
    cookies = ttdowner_html.cookies

    #Attempt to get the api downloads
    ttdowner_api_html = req.post(ttdowner_api, data={'url':url,'token':token}, cookies=cookies)
    if ttdowner_api_html.text == 'error': #Check for error
        return 'error'
    ttdowner_api_parsed = bs(ttdowner_api_html.text, "html.parser")
    ttdowner_api_links = ttdowner_api_parsed.find_all('a')
    
    #Get the links
    links = {}
    links['no_watermark'] = ttdowner_api_links[0]['href']
    links['watermark'] = ttdowner_api_links[1]['href']
    links['audio_only'] = ttdowner_api_links[2]['href']
    
    return links
    
@app.route('/')
def index():
    url = request.args.get('url')
    if (url != None):
        links = ttdowner_get(url)
        return json.dumps(links)
    return 'visit toksaver.com to use the tiktok downloader'

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
