#mypa.py

import speech_recognition as sr			#imports Speech_Recognition Modules
from AppKit import NSSpeechSynthesizer	#imports Speech Synthesizer for tts
from random import randint				#imports randint function
import time								#imports time modules to pause actions
import sys								#imports system functions
import json								#imports json
import urllib
#import pyaudio							#imports pyaudio to play audio
#import wave							#imports .wav conversion

r = sr.Recognizer()									#used to shorten recognizer
cont = True											#used for while loops
playAgain = True
nssp = NSSpeechSynthesizer							#used to shorten apples native speech synthisizer
ve = nssp.alloc().init()							#used to shorten memory allocation and initiation of speech synthisizer
voice = 'com.apple.speech.synthesis.voice.alex'		#voice chosen for speech synthesizer
ve.setVoice_(voice)									#sets appropriate voice
key = '19915fc68b895c6e'							#api key for wunderground

def wakeUp():										#main function, will be used to "wake up" similar to "hey siri"
	while cont:										#ensures that the loop runs continuously
		iSaid = listen()							#listens for my imput
		if iSaid == 'hey bro':						#'hey bro' is the wake up command. This statement checks to see if user wants to do something
			talking('How can I help you sir',2)		#talking funtion called
			selection()									
		else:										#if nothing is said that matches up prints warning and plays sound
			print 'no go'							#warning
			print('\a')								

def preSelection(userText, compare): 										#figures out which commands are being given based on a list of key words
	try:
		myCommand = [userText.find(word) != -1 for word in compare]		 	#creates a true or false array based on what was said
		comInterpreted = [i for i, x in enumerate(myCommand) if x]     		#extracts position of only true responses
		return comInterpreted												#sends back the response
	except AttributeError:													
		print AttributeError												#response when nothing is said


def selection():
	while True:
		iSaid = listen()							#listen function called
		broCommands = ['high','low','quit','current','weather','forecast','rock','paper','scissors','outside'] 		#key words to look out for
		findTruth = preSelection(iSaid, broCommands)
		print findTruth
		if (findTruth == [0,1]):							#'game' command to start hi low game
			playHiLow()								#stars hi low game
		elif (findTruth == [2]):						#'quit command to terminate program
			break									#quits program
		elif (findTruth == [3,4]) or (findTruth == [4,9]):					#'weather' command to get current weather
			currentWeather()						#gets weather
		elif (findTruth == [4,5]):					#'forecast' command to get four day fourcast
			forecast()								#gets forecast
		elif (findTruth == [6,7,8]):		#'rps' command to play rps
			rpsGame()								#plays rps game
	
def talking(text,talkTime):				#(text) are the words that will be said. (talkTime) is the amount of time needed to complete sentence. This function will say the words and ensure that the program pauses so it does not hear itself
	while ve.isSpeaking:				#loop runs while the comp is talking
		ve.startSpeakingString_(text)	#says the text that is passed to the function
		time.sleep(talkTime)			#takes a pause while the computer speaks
		break							
		
def listen():																	#listens to what is being said
	with sr.Microphone() as source:												#determines which mic to use
		print '-'*50
		print ''
		print 'Adjusting for background noise'									#preps to take background noise
		r.adjust_for_ambient_noise(source)										#listens for ambient noise
		print("Set minimum energy threshold to {}".format(r.energy_threshold))	#displays ambient noise adjustment
		print 'I am listining'													#preps to listen to user
		audio = r.listen(source)												#listens to user
	try:
		myWords = r.recognize(audio)											#turns captured audio into text
		print('This time you said:' + myWords)									#prints what you said
		print ''
		return myWords															#returns the text so that it can continue to be used
	except LookupError:															#warns user that the audio could not be interpereted
		talking('I am sorry, I could not understand what you said',3)			

def playHiLow():																				#Higher or Lower Game
	playAgain = True																			#defines play again state
	while playAgain:																			#loop to play game
		numGuess = 0																			#on a new game, number of guesses restarts
		compNum = randint(1,10)																	#computer picks number
		print compNum																			#DELETE LATER display computers number
		talking('I have picked a number between one and ten. Can you guess what it is?',5)		#let user know game has started
		while True:																				#starts loop for current game
			playerGuess = listen()																#listens for players guess
			if playerGuess == 'sex':															#checks for the number 6 (has difficulty understanding difference between 6 and sex)
				playerGuess = '6'																#turns 'sex' into string '6'
			try:																				#checks to see if it can make an integer
				playerGuess = int(playerGuess)													#turns number string into int
			except ValueError:																	#if it can not turn into a string act like it did not understand
				talking('I am sorry, I could not understand what you said',3)					#proclaim ignorance
			if playerGuess == compNum:															#checks for a winning condition
				numGuess += 1																	#adds final count to number of guesses
				text = 'Congratulations! You won in %i guesses!' %(numGuess)					#congratulates the winner
				talking(text,4)																	#says congratulations
				talking('Do you want to play again. Yes or no?',2)								#asks to play again
				reDo = listen()																	#listens for user response
				if reDo == 'yes':																#checks if new game is to be played
					break																		#breaks current loop to start a new game
				else:																			#if anything else is said, assume a quit
					playAgain = False															#signal to end the entire game
					break																		#break current loop
			elif playerGuess < compNum:															#check if players guess is below computers number
				talking('Guess higher',1)														#tell user to guess higher
				numGuess += 1																	#add to guess count
			elif playerGuess > compNum:															#check if players guess is above computers guess
				talking('Guess lower',1)														#tell user to guess lower
				numGuess += 1																	

def getZIP():
	url = 'http://ipinfo.io/json'
	f = urllib.urlopen(url)
	json_string = f.read()
	parsed_json = json.loads(json_string)
	zip = parsed_json['postal']
	city = parsed_json['city']
	state = parsed_json['region']
	data = [zip,city,state]
	return data

def currentWeather():																					#current weather function
    zip = getZIP()																						#listens for zip code
    text = 'getting weather information on ' + zip[1] + ',' + zip[2]
    talking(text, 4)
    url = 'http://api.wunderground.com/api/' + key + '/geolookup/conditions/q/PA/' + zip[0] + '.json'		#goes to wunderground api
    f = urllib.urlopen(url)																				#gets data 
    json_string = f.read()																				#reads data
    parsed_json = json.loads(json_string)																#parses data
    city = parsed_json['location']['city']
    state = parsed_json['location']['state']
    weather = parsed_json['current_observation']['weather']
    temperature_string = parsed_json['current_observation']['temp_f']
    temperature_string = str(temperature_string)
    feelslike_string = parsed_json['current_observation']['feelslike_f']
    weatherText = 'Weather in ' + city + ', ' + state + ': ' + weather.lower() + '. The temperature is ' + temperature_string + ' but it feels like ' + feelslike_string + '.'
    talking(weatherText, 10)
    f.close()

def forecast():																					#four day forecast
    zip = getZIP()																				#listens for zip code
    text = 'getting weather information on ' + zip[1] + ',' + zip[2]
    talking(text, 4)
    url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast/q/' + zip[0] + '.json'	#goes to wunderground api
    f = urllib.urlopen(url)																		#gets data
    json_string = f.read()																		#reads data
    parsed_json = json.loads(json_string)														#parses data
    for day in parsed_json['forecast']['simpleforecast']['forecastday']:						#loop to anounce forecast
    	x = day['date']['day']																	#day is an intiger
    	y = str(x)																				#convert intiger to string
    	forecastText = 'The weather for ' + day['date']['weekday'] + ', ' + day['date']['monthname'] + ' ' + y + ' will be ' + day['conditions'] + ' with a high of ' + day['high']['fahrenheit'] + ' degrees fahrenheit and a low of ' + day['low']['fahrenheit'] + ' degrees farenheit'
        talking(forecastText, 10)
    f.close()

class rpsGame:
	def __init__(self):													#play RPS
		compScore = 0
		playerScore = 0
		tieGame = 0
		player = 0
		playing = True
		validity = True
		talking('Lets play a game of Rock, Paper, Scissors', 3)		#lets player know that the game is starting
		while playing :												#starts loop to play game
			while validity:											#starts loop for player selection
				iSaid = listen()								#listens for player response
				broCommands = ['rock','paper','scissors','quit','Rock'] 		#key words to look out for
				playerHand = preSelection(iSaid, broCommands)
				if (playerHand == [0]) or (playerHand == [4]):							
					player = 1
					break
				elif playerHand == [1]:
					player = 2
					break
				elif playerHand == [2]:
					player = 3
					break
				elif playerHand == [3]:
					player = 4
					break
				else:
					print 'Invalid Choice'
			if player ==4:											#quits game
				if playerScore > compScore:
					text = 'final score, player %i, computer %i, Congratulations you win' % (playerScore, compScore)
				elif playerScore < compScore:
					text = 'final score, player %i, computer %i, Computer wins' % (playerScore, compScore)
				else :
					text = 'final score, player %i, computer %i, tie game' % (playerScore, compScore)
				talking(text, 6)
				break
			
			else:													#starts to determine a winner
				comp = self.compHand()									#gets a "hand" for computer
				result = self.playHand(comp, player)						#gets a result
				playerChoice = self.interpret(player)					#turns numbers into readable text
				compChoice = self.interpret (comp)
				print '\nYou played %s and the computer played %s' % (playerChoice, compChoice)
				talking(result, 2)
				print ''
				print '-'*34
				if result == 'Computer wins!':
					compScore += 1
				elif result == 'Player wins!':
					playerScore += 1
				elif result == 'Tie game':
					tieGame += 1
				print 'Player: %i Computer: %i Tie Games: %i' % (playerScore, compScore, tieGame)
				print '-'*34
				print ''
							
	def compHand(self):					#needed for rps game
		compVal = randint(1,3)
		return compVal
		
	def interpret(self,num):				#needed for rps game
		if num == 1:
			talking('Rock', 1)
			return 'Rock'
		elif num == 2:
			talking('Paper', 1)
			return 'Paper'
		elif num == 3:
			talking('Scissors', 1)
			return 'Scissors'
	
	def playHand(self,comp, player):		#needed for rps game
		if comp == player:
			return 'Tie game'
		if (comp == 1 and player == 3) or (comp == 2 and player == 1) or (comp == 3 and player == 2):
			return 'Computer wins!'
		else:
			return 'Player wins!'










"""
	if myWords == "run":																#looks for 'run' command to run the hi low game
	    print 'got it'
	    import hi_lowGame
	elif myWords == "game":																#looks for 'game' command to run rps game
	    print 'starting game'
	    import rps_game
	else:																				#lets user know that the command does not do anything
		print 'not a command'
		
import random

"""
wakeUp()