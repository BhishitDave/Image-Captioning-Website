from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import JSONMixin 
import requests
from caption import *
import warnings
warnings.filterwarnings("ignore")

apikey=''
with open('apikey.txt') as f:
    apikey = f.read()

app = Flask(__name__)


@app.route('/')
def start_up_route():
	return render_template('index.html')



@app.route('/', methods = ['POST'])
def upload_file():
	try:
		if request.method == 'POST':
			img = request.files['image']

			# print(img)
			# print(img.filename)

			img.save("static/"+img.filename)

	
			caption = caption_this_image("static/"+img.filename)

			result_dic = {
				'image' : "static/" + img.filename,
				'description' : caption
			}
			return render_template('index.html', results = result_dic)
	except:
		print("error")

@app.route('/upload', methods =["GET", "POST"])	
def microsoftapi():
    if request.method == "POST":
       link = request.form.get("urls")
       url = "https://microsoft-computer-vision3.p.rapidapi.com/describe"
       querystring = {"language":"en","maxCandidates":"1","descriptionExclude":"Celebrities"}
       payload = "{\r\"url\": \""+link+ "\"\r}"
       headers = {
        'content-type': "application/json",
        'x-rapidapi-key': apikey,
        'x-rapidapi-host': "microsoft-computer-vision3.p.rapidapi.com"
        }
       response = requests.request("POST", url, data=payload, headers=headers, params=querystring).json()

       data=response
       print(response)
       try:
          caption=data['description']['captions'][0]['text']
       except:
          caption="Not a valid link"
       result_dic = {
				'image' : link,
				'description' : caption
       }
       print('YES')
       return render_template("index.html",result=result_dic)


if __name__ == '__main__':
	app.run(debug = True)