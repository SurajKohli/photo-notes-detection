import os
import kivy

from kivy.app import App
kivy.require("1.8.0")

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class AppScreen(GridLayout):

	def run_definition_scraping(self,instance):
		print("Finally Scraping !! Yaay !! :) ")
		word_list = self.word_list.text.split('\n')
		for i in word_list:
			os.system('python3 final_definition_scraper.py ' + str(i))

		topic_list = self.topic_list.text.split('\n')
		for i in topic_list:
			print(i)
			os.system('python3 final_tutorialspoint_scraper.py "' + str(i) + '"')

		if hasattr(self,'scraping_result'):
			self.topic_result.text = "[b][i][color=bfabfa]Finished Scraping. !! :) CHECK RESULT FOLDER FOR RESULTS[/color][/i][/b]"
		else:
			self.topic_result = Label(text= "[b][i][color=bfabfa]Finished Scraping. !! :) CHECK RESULT FOLDER FOR RESULTS[/color][/i][/b]", markup=True, font_size=20)
			self.add_widget(self.topic_result)



	def save_topic_list(self,instance,value):
		with open('Result/topic_list.txt','w') as f:
			f.write(self.topic_list.text)
		f.close()

	def run_topic_finding(self,instance):
		os.system('python3 final_finding_topic.py')
		if hasattr(self,'topic_result'):
			self.topic_result.text = "F[b][i][color=bfabfa]Finished Finding Topic :) [/color][/i][/b]"
		else:
			self.topic_result = Label(text= "[b][i][color=bfabfa]Finished Finding Topic :) [/color][/i][/b]", markup=True, font_size=25)
			self.add_widget(self.topic_result)
		self.add_widget(Label(text="[b][color=bfabfa]Topic Found. Modify to suit your needs[/color][/b]", markup=True, font_size=25))
		self.topic_list = TextInput(multiline=True)
		with open('Result/topic_list.txt','r') as f:
			topic_list = f.read()
		f.close()
		self.add_widget(self.topic_list)
		self.topic_list.text = topic_list
		self.topic_list.bind(text=self.save_topic_list)
		# self.topic_list.background_color = [255,255,0,0.8]
		self.topic_list.background_normal = "orange.png"
		self.topic_list.cursor_color = [255,0,0,0.3]
		self.topic_list.font_size = 30
		self.definition_scraping = Button(text="Run Scraping", font_size=25, on_press=self.run_definition_scraping, background_normal="orange.png", color=[125,121,117,1])
		self.add_widget(self.definition_scraping)

	def save_word_list(self,instance,value):
		print(self.word_list.text)
		print(instance)
		print(value)
		with open('Result/word_list.txt','w') as f:
			f.write(self.word_list.text)
		f.close()

	def topic_editing(self):
		self.add_widget(Label(text="[b][color=bfabfa]Words Found. Modify to suit your needs[/color][/b]", markup=True, font_size=25))
		self.word_list = TextInput(multiline=True)
		with open('Result/word_list.txt','r') as f:
			word_list = f.read()
		f.close()
		self.add_widget(self.word_list)
		self.word_list.text = word_list
		self.word_list.bind(text=self.save_word_list)
		# self.word_list.background_color = [255,255,0,0.8]
		self.word_list.background_normal = "orange.png"
		self.word_list.cursor_color = [255,0,0,0.3]
		self.word_list.font_size = 30
		self.topic_finding = Button(text="Run Topic Finding ", font_size=25, on_press=self.run_topic_finding,background_normal="orange.png", color=[125,121,117,1])
		self.add_widget(self.topic_finding)

	def run_word_detection(self,instance):
		print("Running Word detection !!")
		os.system('python3 generate_word_contours.py ' + str(self.file_name.text) + ' Result')
		for file_name in os.listdir('./Result'):
			if file_name == 'contoured.jpg':
				pass
			else:
				os.system('python3 final_train_test.py Result/' + str(file_name))
		print(self.file_name.text)
		if hasattr(self,'word_result'):
			self.word_result.text = "[b][i][color=bfabfa]Finished detecting Words. !! :)[/color][/i][/b]"
		else:
			self.word_result = Label(text= "[b][i][color=bfabfa]Finished detecting Words. !! :)[/color][/i][/b]" , markup=True, font_size=25)
			self.add_widget(self.word_result)
		self.topic_editing()

	def __init__(self, **kwargs):
		super(AppScreen, self).__init__(**kwargs)
		self.cols = 2
		self.row = 7
		self.row_force_default = True
		self.row_default_height = 100
		self.add_widget(Label(text='[b][color=bfabfa]Enter the name of the Image File[/color][/b]', markup=True, font_size=25 ))
		self.file_name = TextInput(multiline=False)
		# self.file_name.background_color = [255,255,0,0.8]
		self.file_name.background_normal = "orange.png"
		self.file_name.cursor_color = [255,0,0,0.3]
		self.file_name.font_size = 30
		self.add_widget(self.file_name)
		self.word_detec = Button(text="Run Word Detection", font_size=25, on_press=self.run_word_detection, background_normal="orange.png", color=[125,121,117,1])
		self.add_widget(self.word_detec)

class photoNotes(App):
	def build(self):
		return AppScreen()

if __name__ == "__main__":
	Window.size = (1200,1200)
	photoNotes().run()