# Import requiements
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create our class
class InstagramBot:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.bot = webdriver.Firefox()	

	# Function will log us in to Instagram
	def login(self):
		bot = self.bot
		# Navigate to the Instagram login page
		bot.get('https://www.instagram.com/accounts/login/')
		time.sleep(3)

		# Find the email and password boxes, enter our login credentials
		email = bot.find_element_by_name('username').send_keys(self.username)
		password = bot.find_element_by_name('password').send_keys(self.password)

		# Wait for 1 second then press ENTER
		time.sleep(1)
		bot.find_element_by_name('password').send_keys(Keys.RETURN)

		# Wait 3 second while the post-login page loads
		time.sleep(3)

	def findMyFollowers(self, number_of_followers):
		bot = self.bot

		bot.get('https://instagram.com/' + self.username)
		time.sleep(2)

		seg = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
		if number_of_followers == 0:
			number_of_followers = int(seg)
		print("tenho:",number_of_followers,"seguidores")

		bot.find_element_by_xpath('//a[@href="/' + self.username + '/followers/"]').click()

		time.sleep(1)

		popup = bot.find_element_by_class_name('isgrP')

		followers_array = []

		i = 1
		#print("sua lista tem",len(followers_array),"elementos")
		while len(followers_array) < number_of_followers:
			bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', popup)
			time.sleep(1)

			followers = bot.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')
			# print("Todos os seguidores: ",followers)
			for follower in followers:
				# follower.txt mostra o seguidor atual
				# print("Seguidores coletados: ", followers_array)
				if follower.text not in followers_array:
					followers_array.append(follower.text)
					followers_array = list( dict.fromkeys(followers_array) )

			i+=1
		print("Seguidores coletados: ", len(followers_array))

		#print("sua nova lista tem", len(followers_array),"elementos")

		with open("seguidores.txt", "w") as txt:
		    for line in followers_array:
		        txt.write("".join(line) + "\n") # works with any number of elements in a line


		self.followers = followers_array

	def followTheirFollowers(self, number_to_follow):
		bot = self.bot
		print("Seguirei",number_to_follow,"perfis de cada perfil coletado!")

		for follower in self.followers:
			bot.get('https://instagram.com/' + follower)

			time.sleep(5) # Tempo para esperar antes de começar a seguir

			if(len(bot.find_elements_by_xpath("//*[contains(text(), 'This Account is Private')]")) > 0):
				# If they're private, we can't see their follower list, so skip them
				print("Private profile")
				continue

			bot.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
			
			time.sleep(3)
			

			follow = bot.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
			#following = bot.find_elements_by_xpath("//button[contains(text(), 'Following')]")
			#requested = bot.find_elements_by_xpath("//button[contains(text(), 'Requested')]")
			#print("Following funciona? ", bot.find_elements_by_xpath("//button[contains(text(), 'Following')]"))
			#a = bot.find_element_by_css_selector('button')

			i = 1

			for followButton in follow:
				print("Pos:", i)
				# follower = bot.find_element_by_css_selector(".FPmhX.notranslate._0imsa").text
				if followButton.text == "Following" or followButton.text == "Requested":
					i+=1
					continue
				bot.execute_script("arguments[0].click();", followButton)
				# print("Tentando seguir o",followButton)

				if(i > number_to_follow):
					break

				i+=1
				if i == 8:
					bot.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', bot.find_element_by_class_name('isgrP'))
				time.sleep(10) # Intervalo de tempo à seguir novos perfis

			time.sleep(5) # Intervalo de tempo pra ir pro próximo perfil


insta = InstagramBot('usuario', 'senha') # colocar em um txt dps pra n precisar colocar aqui
insta.login()
insta.findMyFollowers(0) # Encontra quantos seguidores o perfil tem
insta.followTheirFollowers(10) # Define quantos seguidores em comum o script vai seguir