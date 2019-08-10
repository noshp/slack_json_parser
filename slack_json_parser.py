#! python3
# slack_json_parser.py - some tools for parsing the json that you can download from Slack

import json, os, pandas, sys


class Parser:
	def __init__(self):
		self.static_dir = "."
		self.data_dir = self.static_dir+"/data/"

		self.user_data_file = json.load( open(self.data_dir+"/users.json") )
		self.channel_data_file = json.load( open(self.data_dir+"/channels.json") )

		self.user_info = self.get_user_info()
		
		self.dirs = [dir for dir in os.listdir(self.data_dir) if "." not in dir]


	def get_user_info(self):
		channels = {}

		for user in self.user_data_file:
			try:
				if user['is_bot'] == False:
					channels[ user['id'] ] = {"name" : user["real_name"], "channels" : [] }
			except:
				continue

		for channel in self.channel_data_file:
			for member in channel["members"]:
				
				try:
					channels[member]["channels"].append( channel["name"] )
				except:
					pass

		return channels


	def file_to_dict(self, file):
		with open(file) as input:
			input_json = json.load(input)
			return input_json


	def get_messages(self):
		messages = []
		for dir in self.dirs:
			for file in os.listdir(self.data_dir+dir):
				input_dict = self.file_to_dict(self.data_dir+dir+"/"+file)
				for object in input_dict:
					try:
						messages.append( 
						{
						"user_name": object["user_profile"]["real_name"],
						"message": object["text"],
						"channel": dir,
						"timestamp": object["ts"]
						} )
					
					except:
						continue
		return messages

	def get_reactions(self):
		reactions = []
		for dir in self.dirs:
			for file in os.listdir(self.data_dir+dir):
				input_dict = self.file_to_dict(self.data_dir+dir+"/"+file)
				for object in input_dict:
					try:
						for reaction in object["reactions"]:
							reactions.append(
							{
								"reaction" : reaction["name"],
								"user_ids" : reaction["users"]
							})

					except:
						continue
		return reactions

	def return_csv(self):
		# To do later?
		input = self.get_messages()
		output = {
			"user_name": [],
			"message": [],
			"channel": [],
			"timestamp": []
		}
		for object in input:
			output["user_name"].append( object["user_name"] )
			output["message"].append( object["message"] )
			output["channel"].append( object["channel"] )
			output["timestamp"].append( object["timestamp"] )
		
		return output





class Analyzer:
	def __init__(self, messages, users):
		self.messages = messages
		self.messages_dataframe = pandas.DataFrame( self.messages, columns = ["user_name", "message", "channel", "timestamp"] )

		# add metadata
		self.messages_dataframe["word_count"] = len( self.messages_dataframe["message"] )


	def count_words_per_user(self):
		# WIP
		
		# number of words per user
		return self.messages_dataframe.groupby(["user_name"]).sum().to_csv()


	def count_words_per_user_per_channel
		return self.messages_dataframe.groupby(["user_name", "channel"]).sum().to_csv()


	def count_words_per_user_per_day
		pass



if __name__ == "__main__":
	par = Parser()
	
	messages = par.return_csv()
	users = par.get_user_info()

	ana = Analyzer( messages, users )
	ana.count_messages()

	with open("message_stats.csv", 'w') as output:
		output.write( ana.count_messages() ) 
		output.close()

	#print( par.get_user_info() )






