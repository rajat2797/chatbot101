# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re
from chatbot.models import Users
# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
# Create your views here.

# DEVELOPER_KEY = 'AIzaSyAfkPZzhdm2e3c1V8F4t_3RkwvCVQghz8k'
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

url_google = 'https://www.googleapis.com/youtube/v3/search'

pokemon_data = {"Bulbasaur":"http://img.pokemondb.net/artwork/bulbasaur.jpg","Ivysaur":"http://img.pokemondb.net/artwork/ivysaur.jpg","Venusaur":"http://img.pokemondb.net/artwork/venusaur.jpg","Charmander":"http://img.pokemondb.net/artwork/charmander.jpg","Charmeleon":"http://img.pokemondb.net/artwork/charmeleon.jpg","Charizard":"http://img.pokemondb.net/artwork/charizard.jpg","Squirtle":"http://img.pokemondb.net/artwork/squirtle.jpg","Wartortle":"http://img.pokemondb.net/artwork/wartortle.jpg","Blastoise":"http://img.pokemondb.net/artwork/blastoise.jpg","Caterpie":"http://img.pokemondb.net/artwork/caterpie.jpg","Metapod":"http://img.pokemondb.net/artwork/metapod.jpg","Butterfree":"http://img.pokemondb.net/artwork/butterfree.jpg","Weedle":"http://img.pokemondb.net/artwork/weedle.jpg","Kakuna":"http://img.pokemondb.net/artwork/kakuna.jpg","Beedrill":"http://img.pokemondb.net/artwork/beedrill.jpg","Pidgey":"http://img.pokemondb.net/artwork/pidgey.jpg","Pidgeotto":"http://img.pokemondb.net/artwork/pidgeotto.jpg","Pidgeot":"http://img.pokemondb.net/artwork/pidgeot.jpg","Rattata":"http://img.pokemondb.net/artwork/rattata.jpg","Raticate":"http://img.pokemondb.net/artwork/raticate.jpg","Spearow":"http://img.pokemondb.net/artwork/spearow.jpg","Fearow":"http://img.pokemondb.net/artwork/fearow.jpg","Ekans":"http://img.pokemondb.net/artwork/ekans.jpg","Arbok":"http://img.pokemondb.net/artwork/arbok.jpg","Pikachu":"http://img.pokemondb.net/artwork/pikachu.jpg","Raichu":"http://img.pokemondb.net/artwork/raichu.jpg","Sandshrew":"http://img.pokemondb.net/artwork/sandshrew.jpg","Sandslash":"http://img.pokemondb.net/artwork/sandslash.jpg","Nidoran":"http://vignette1.wikia.nocookie.net/pokemon/images/2/22/029Nidoran_AG_anime.png/revision/latest?cb=20140914053937","Nidorina":"http://img.pokemondb.net/artwork/nidorina.jpg","Nidoqueen":"http://img.pokemondb.net/artwork/nidoqueen.jpg","Nidorino":"http://img.pokemondb.net/artwork/nidorino.jpg","Nidoking":"http://img.pokemondb.net/artwork/nidoking.jpg","Clefairy":"http://img.pokemondb.net/artwork/clefairy.jpg","Clefable":"http://img.pokemondb.net/artwork/clefable.jpg","Vulpix":"http://img.pokemondb.net/artwork/vulpix.jpg","Ninetales":"http://img.pokemondb.net/artwork/ninetales.jpg","Jigglypuff":"http://img.pokemondb.net/artwork/jigglypuff.jpg","Wigglytuff":"http://img.pokemondb.net/artwork/wigglytuff.jpg","Zubat":"http://img.pokemondb.net/artwork/zubat.jpg","Golbat":"http://img.pokemondb.net/artwork/golbat.jpg","Oddish":"http://img.pokemondb.net/artwork/oddish.jpg","Gloom":"http://img.pokemondb.net/artwork/gloom.jpg","Vileplume":"http://img.pokemondb.net/artwork/vileplume.jpg","Paras":"http://img.pokemondb.net/artwork/paras.jpg","Parasect":"http://img.pokemondb.net/artwork/parasect.jpg","Venonat":"http://img.pokemondb.net/artwork/venonat.jpg","Venomoth":"http://img.pokemondb.net/artwork/venomoth.jpg","Diglett":"http://img.pokemondb.net/artwork/diglett.jpg","Dugtrio":"http://img.pokemondb.net/artwork/dugtrio.jpg","Meowth":"http://img.pokemondb.net/artwork/meowth.jpg","Persian":"http://img.pokemondb.net/artwork/persian.jpg","Psyduck":"http://img.pokemondb.net/artwork/psyduck.jpg","Golduck":"http://img.pokemondb.net/artwork/golduck.jpg","Mankey":"http://img.pokemondb.net/artwork/mankey.jpg","Primeape":"http://img.pokemondb.net/artwork/primeape.jpg","Growlithe":"http://img.pokemondb.net/artwork/growlithe.jpg","Arcanine":"http://img.pokemondb.net/artwork/arcanine.jpg","Poliwag":"http://img.pokemondb.net/artwork/poliwag.jpg","Poliwhirl":"http://img.pokemondb.net/artwork/poliwhirl.jpg","Poliwrath":"http://img.pokemondb.net/artwork/poliwrath.jpg","Abra":"http://img.pokemondb.net/artwork/abra.jpg","Kadabra":"http://img.pokemondb.net/artwork/kadabra.jpg","Alakazam":"http://img.pokemondb.net/artwork/alakazam.jpg","Machop":"http://img.pokemondb.net/artwork/machop.jpg","Machoke":"http://img.pokemondb.net/artwork/machoke.jpg","Machamp":"http://img.pokemondb.net/artwork/machamp.jpg","Bellsprout":"http://img.pokemondb.net/artwork/bellsprout.jpg","Weepinbell":"http://img.pokemondb.net/artwork/weepinbell.jpg","Victreebel":"http://img.pokemondb.net/artwork/victreebel.jpg","Tentacool":"http://img.pokemondb.net/artwork/tentacool.jpg","Tentacruel":"http://img.pokemondb.net/artwork/tentacruel.jpg","Geodude":"http://img.pokemondb.net/artwork/geodude.jpg","Graveler":"http://img.pokemondb.net/artwork/graveler.jpg","Golem":"http://img.pokemondb.net/artwork/golem.jpg","Ponyta":"http://img.pokemondb.net/artwork/ponyta.jpg","Rapidash":"http://img.pokemondb.net/artwork/rapidash.jpg","Slowpoke":"http://img.pokemondb.net/artwork/slowpoke.jpg","Slowbro":"http://img.pokemondb.net/artwork/slowbro.jpg","Magnemite":"http://img.pokemondb.net/artwork/magnemite.jpg","Magneton":"http://img.pokemondb.net/artwork/magneton.jpg","Farfetch'd":"http://vignette3.wikia.nocookie.net/pokemon/images/6/61/083Farfetch'd_AG_anime.png/revision/latest?cb=20140810002805","Doduo":"http://img.pokemondb.net/artwork/doduo.jpg","Dodrio":"http://img.pokemondb.net/artwork/dodrio.jpg","Seel":"http://img.pokemondb.net/artwork/seel.jpg","Dewgong":"http://img.pokemondb.net/artwork/dewgong.jpg","Grimer":"http://img.pokemondb.net/artwork/grimer.jpg","Muk":"http://img.pokemondb.net/artwork/muk.jpg","Shellder":"http://img.pokemondb.net/artwork/shellder.jpg","Cloyster":"http://img.pokemondb.net/artwork/cloyster.jpg","Gastly":"http://img.pokemondb.net/artwork/gastly.jpg","Haunter":"http://img.pokemondb.net/artwork/haunter.jpg","Gengar":"http://img.pokemondb.net/artwork/gengar.jpg","Onix":"http://img.pokemondb.net/artwork/onix.jpg","Drowzee":"http://img.pokemondb.net/artwork/drowzee.jpg","Hypno":"http://img.pokemondb.net/artwork/hypno.jpg","Krabby":"http://img.pokemondb.net/artwork/krabby.jpg","Kingler":"http://img.pokemondb.net/artwork/kingler.jpg","Voltorb":"http://img.pokemondb.net/artwork/voltorb.jpg","Electrode":"http://img.pokemondb.net/artwork/electrode.jpg","Exeggcute":"http://img.pokemondb.net/artwork/exeggcute.jpg","Exeggutor":"http://img.pokemondb.net/artwork/exeggutor.jpg","Cubone":"http://img.pokemondb.net/artwork/cubone.jpg","Marowak":"http://img.pokemondb.net/artwork/marowak.jpg","Hitmonlee":"http://img.pokemondb.net/artwork/hitmonlee.jpg","Hitmonchan":"http://img.pokemondb.net/artwork/hitmonchan.jpg","Lickitung":"http://img.pokemondb.net/artwork/lickitung.jpg","Koffing":"http://img.pokemondb.net/artwork/koffing.jpg","Weezing":"http://img.pokemondb.net/artwork/weezing.jpg","Rhyhorn":"http://img.pokemondb.net/artwork/rhyhorn.jpg","Rhydon":"http://img.pokemondb.net/artwork/rhydon.jpg","Chansey":"http://img.pokemondb.net/artwork/chansey.jpg","Tangela":"http://img.pokemondb.net/artwork/tangela.jpg","Kangaskhan":"http://img.pokemondb.net/artwork/kangaskhan.jpg","Horsea":"http://img.pokemondb.net/artwork/horsea.jpg","Seadra":"http://img.pokemondb.net/artwork/seadra.jpg","Goldeen":"http://img.pokemondb.net/artwork/goldeen.jpg","Seaking":"http://img.pokemondb.net/artwork/seaking.jpg","Staryu":"http://img.pokemondb.net/artwork/staryu.jpg","Starmie":"http://img.pokemondb.net/artwork/starmie.jpg","Mr. Mime":"http://guidesarchive.ign.com/guides/9846/images/mrmime.gif","Scyther":"http://img.pokemondb.net/artwork/scyther.jpg","Jynx":"http://img.pokemondb.net/artwork/jynx.jpg","Electabuzz":"http://img.pokemondb.net/artwork/electabuzz.jpg","Magmar":"http://img.pokemondb.net/artwork/magmar.jpg","Pinsir":"http://img.pokemondb.net/artwork/pinsir.jpg","Tauros":"http://img.pokemondb.net/artwork/tauros.jpg","Magikarp":"http://img.pokemondb.net/artwork/magikarp.jpg","Gyarados":"http://img.pokemondb.net/artwork/gyarados.jpg","Lapras":"http://img.pokemondb.net/artwork/lapras.jpg","Ditto":"http://img.pokemondb.net/artwork/ditto.jpg","Eevee":"http://img.pokemondb.net/artwork/eevee.jpg","Vaporeon":"http://img.pokemondb.net/artwork/vaporeon.jpg","Jolteon":"http://img.pokemondb.net/artwork/jolteon.jpg","Flareon":"http://img.pokemondb.net/artwork/flareon.jpg","Porygon":"http://img.pokemondb.net/artwork/porygon.jpg","Omanyte":"http://img.pokemondb.net/artwork/omanyte.jpg","Omastar":"http://img.pokemondb.net/artwork/omastar.jpg","Kabuto":"http://img.pokemondb.net/artwork/kabuto.jpg","Kabutops":"http://img.pokemondb.net/artwork/kabutops.jpg","Aerodactyl":"http://img.pokemondb.net/artwork/aerodactyl.jpg","Snorlax":"http://img.pokemondb.net/artwork/snorlax.jpg","Articuno":"http://img.pokemondb.net/artwork/articuno.jpg","Zapdos":"http://img.pokemondb.net/artwork/zapdos.jpg","Moltres":"http://img.pokemondb.net/artwork/moltres.jpg","Dratini":"http://img.pokemondb.net/artwork/dratini.jpg","Dragonair":"http://img.pokemondb.net/artwork/dragonair.jpg","Dragonite":"http://img.pokemondb.net/artwork/dragonite.jpg","Mewtwo":"http://img.pokemondb.net/artwork/mewtwo.jpg","Mew":"http://img.pokemondb.net/artwork/mew.jpg"}

VERIFY_TOKEN='7thseptember2016'

PAGE_ACCESS_TOKEN='EAAJmjf94eZB8BAEJHwLBtA5RxiIR6WUhra7TiXXIZBHrFtV7ZCyUFGuPOpG2O9vWMa2Lc8w5IFQZA1aZCHPqP4eZCrZCAcGQgYrcubYnVcD2jGF8ems2ZAUfQARhR6ivnofruOF2cSLKVVGEW8lOcYYh2FZBZCioJFDeHnZAy5PKcu1oQZDZD'

weather_api='b82cf7a4b0f1881c7a0513246b4adb28'

def post_img(fbid,image_url):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg=json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image","payload":{"url":image_url}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def default(fbid):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text = "Hi! I'm not yet programmed to be talking to a person. Type 'hi' to know the format of the operations" 
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def blog(fbid,name,query):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	p = Users.objects.get(user_name=name)
	output_text = ''
	if query=='show':
		output_text += 'TITLE :\n%s\n'%(p.title.encode('utf-8'))
		output_text += 'CONTENT :\n%s\n'%(p.content.encode('utf-8'))
	else:
		output_text = 'Changes have made successfully'
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def display(fbid,message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

# def youtube_search2(options):
#    	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
#   	search_response = youtube.search().list(
# 	    q=options.q,
# 	    type="video",
# 	    location=options.location,
# 	    locationRadius=options.location_radius,
# 		part="id,snippet",
# 		maxResults=options.max_results
# 		).execute()


def weather(fbid,city):
	url='http://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s'%(city,weather_api)
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	resp = requests.get(url=url).text
	data = json.loads(resp)
	temp=float(data['main']['temp']) - 273.15
	min_temp=float(data['main']['temp_min']) - 273.15
	max_temp=float(data['main']['temp_max']) - 273.15
	output_text='City : %s\nTemp = %.2f degree celcius\nMin. Temp = %.2f degree celcius\nMax. Temp = %.2f degree celcius'%(city,temp,min_temp,max_temp)
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def youtube_search(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text='https://www.youtube.com/results?search_query=%s'%(message_text)
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text":message_text.capitalize().replace('+',' '),"buttons":[{"type":"web_url","url":output_text,"title":"OPEN"}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def youtube_mp3(fbid,message_text):
	url='www.youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com/watch?v=%s'%(message_text)

def movies(fbid,title):
	url='http://www.omdbapi.com/?t=%s&y=&plot=short&r=json'%(title)
	resp = requests.get(url=url).text
	data = json.loads(resp)
	output_text=''
	t=data['Title']
	y=data['Year']
	r=data['imdbRating']
	g=data['Genre']
	p=data['Plot']
	a=data['Actors']
	img=data['Poster']
	post_img(fbid,img)
	output_text='Title : %s\nYear : %s\nIMDB-Rating : %s\nGenre : %s\nActors : %s\nPlot : %s'%(t,y,r,g,a,p)

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def post_button(fbid,url):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid},"message":{"attachment":{"type":"template","payload":{"template_type":"button","text":"Open Link","buttons":[{"type":"web_url","url":url,"title":"Open Link"}]}}}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def wikisearch(fbid,title='tomato'):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s'%(title)
    resp = requests.get(url=url).text
    data = json.loads(resp)
    scoped_data = data['query']['pages']
    print scoped_data
    page_id = data['query']['pages'].keys()[0]
    wiki_url = 'https://en.m.wikipedia.org/?curid=%s'%(page_id)
    try:
        wiki_content = scoped_data[page_id]['extract']
        wiki_content = re.sub(r'[^\x00-\x7F]+',' ', wiki_content)
        wiki_content = re.sub(r'\([^)]*\)', '', wiki_content)
        
        if len(wiki_content) > 315:
            wiki_content = wiki_content[:315] + ' ...'

    except KeyError:
        wiki_content = ''

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": wiki_content}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def intro(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text="Hi there! I'm a ChatBot\nType :\n#wiki WORD - Wikipedia Search\n#Pokemon POKEMON NAME - Pokemon Search\n#movie MOVIE NAME - Movie details,rating etc..\n#youtube TITLE - Youtube Search\n#weather CITY NAME/COUNTRY NAME\n#blog USERS - To list all users\n#blog USERNAME SHOW\n#blog USERNAME ADD TITLE & CONTENT"
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def pokemon(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	result_arr=[]
	for k,v in pokemon_data.iteritems():
		if message_text.lower() in k.lower():
			result_arr.append([k,v])

	output_text=''
	for i in result_arr:
		output_text+=i[0]
		output_text+='\n'
		output_text+=i[1]
		output_text+='\n'
		post_img(fbid,i[1])

	if output_text=='':
		output_text='Kindly type a pokemon name'
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	post_button(fbid,output_text)

def logg(message,symbol='-'):
	print '%s\n %s\n %s\n'%(symbol*10,message,symbol*10)

class MyChatBotView(generic.View):
	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message=json.loads(self.request.body.decode('utf-8'))
		logg(incoming_message)
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					# post_img(sender_id)
					if message_text.lower()=='hi' or message_text.lower()=='hello' or message_text.lower()=='hey' or message_text.lower()=='yo' or message_text.lower()=='hi!' or message_text.lower()=='hello!' or message_text.lower()=='hey!' or message_text.lower()=='yo!':
						intro(sender_id,message_text)
					elif '#pokemon' in message_text.split(" ")[0].lower():
						message_text = message_text.split(" ")
						pokemon(sender_id,message_text[1])
					elif '#wiki' in message_text.split(" ")[0].lower():
						message_text = message_text.split(" ",1)
						wikisearch(sender_id,message_text[1].replace(' ','%20'))
					elif '#movie' in message_text.split(" ")[0].lower():
						message_text = message_text.split(" ",1)
						movies(sender_id,message_text[1].replace(' ','+').lower())
					elif '#youtube' in message_text.split(" ")[0].lower():
						message_text = message_text.split(" ",1)
						youtube_search(sender_id,message_text[1].replace(' ','+').lower())
					elif '#blog' in message_text.split(" ")[0].lower():
						if 'users' in message_text.split(" ")[1].lower():
							u = Users.objects.all()
							message_text = ''
							for i in u:
								message_text+= i.user_name+'\n'
							display(sender_id,message_text)
						else:
							message_text = message_text.split(' ',3)
							name= message_text[1]
							query = message_text[2].lower()
							u,created = Users.objects.get_or_create(user_name=name)
							if 'add' in query:
								part=message_text[3].split('&')
								u.title = part[0].rstrip()
								u.content = part[1].lstrip()
								u.save()
								blog(sender_id,name,query)
							else:
								blog(sender_id,name,query)
					elif '#weather' in message_text.split(" ")[0].lower():
						message_text = message_text.split(' ',1)
						weather(sender_id,message_text[1])
					else:
						default(sender_id)
				except Exception as e:
					print e
					pass

		return HttpResponse() 

def index(request):
	return HttpResponse('hello')