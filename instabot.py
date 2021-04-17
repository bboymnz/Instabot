from time import sleep
from selenium import webdriver
from login_info import pw,user
followers=[]
following=[]
not_following_back=[]
class Instabot():
    def __init__(self,username,password):
        self.username=username
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.instagram.com/')
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath('//button[text()="Not Now"]')\
            .click()
        sleep(2)

    def get_unfollowers(self):
        global followers
        global following
        global not_following_back
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2) 
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following=self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers=self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)
        
        
    
    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        print(names)

        self.driver.find_element_by_css_selector("html.js.logged-in.client-root.js-focus-visible.sDN5V body div.RnEpo.Yx5HN div.pbNvD.fPMEg.HYpXt div._1XyCr div div.eiUFA div.WaOAr button.wpO6b")\
            .click()
        return names
       
       
          

my_bot=Instabot(user,pw)
my_bot.get_unfollowers()

with open('following.txt','w') as f:
  f.write('\n'.join(following))

with open('followers.txt','w') as f1:
  f1.write('\n'.join(followers))

with open('Not_following_back.txt','w') as f2:
  f2.write('\n'.join(not_following_back))


