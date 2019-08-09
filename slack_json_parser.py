#! python3
# slack_json_parser.py - some tools for parsing the json that you can download from Slack

import json, os

class Parser:
	def __init__(self):
		self.static_dir = "."
		self.data_dir = self.static_dir+"/data/"

		self.user_data_file = json.load( open(self.data_dir+"/users.json") )

		self.user_ids = self.get_user_id()
		
		self.dirs = [dir for dir in os.listdir(self.data_dir) if "." not in dir]


	def get_user_id(self):
		users = []
		for user in self.user_data_file:
			try:
				if user['is_bot'] == False:
					users.append( {"user_id" : user['id'], "user_name" : user["real_name"]} )
			except:
				continue

		return users


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
						messages.append( {
						"user_id": object["user"],
						"message": object["text"]

						} )

					
					except:
						continue
		return messages




if __name__ == "__main__":
	bot = Parser()
	with open("messages.json", 'w') as output:
			output.write( json.dumps( bot.get_messages() ) )
			output.close()
