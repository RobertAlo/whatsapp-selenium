import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
try:
    import autoit
except:
    pass
import time
import datetime
import os

import csv

browser = None
Contact = None
message = None
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None

def input_contacts():
    global Contact,unsaved_Contacts
    # List of Contacts
    Contact = []
    unsaved_Contacts = []
    while True:
        # Enter your choice 1 or 2
        print("PLEASE CHOOSE ONE OF THE OPTIONS:\n")
        print("1.Message to Saved Contact number")
        print("2.Message to Unsaved Contact number\n")
        x = int(input("Enter your choice(1 or 2):\n"))
        print()
        if x == 1:
            n = int(input('Enter number of Contacts to add(count)->'))
            print()
            for i in range(0,n):
                inp = str(input("Enter contact name(text)->"))
                inp = '"' + inp + '"'
                # print (inp)
                Contact.append(inp)
        elif x == 2:
            n = int(input('Enter number of unsaved Contacts to add(count)->'))
            print()
            for i in range(0,n):
                # Example use: 919899123456, Don't use: +919899123456
                # Reference : https://faq.whatsapp.com/en/android/26000030/
                inp = str(input("Enter unsaved contact number with country code(interger):\n\nValid input: 91943xxxxx12\nInvalid input: +91943xxxxx12\n\n"))
                # print (inp)
                unsaved_Contacts.append(inp)

        choi = input("Do you want to add more contacts(y/n)->")
        if choi == "n":
            break

    if len(Contact) != 0:
        print("\nSaved contacts entered list->",Contact)
    if len(unsaved_Contacts) != 0:
        print("Unsaved numbers entered list->",unsaved_Contacts)
    input("\nPress ENTER to continue...")

def input_message():
    global message
    # Enter your Good Morning Msg
    print()
    print("Ingrese el mensaje y use el simbolo '~' para terminar un mensaje:\nPor ejemmplo: Hola mudo!~\n\nSu mensaje: ")
    message = []
    temp = ""
    done = False

    while not done:
      temp = input()
      if len(temp)!=0 and temp[-1] == "~":
        done = True
        message.append(temp[:-1])
      else:
        message.append(temp)
    message = "\n".join(message)
    print()
    print(message)

def whatsapp_login():
    global wait,browser,Link
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 28800)
    #el icono de chat como señal de qr escaneado
    chat = 'span[data-icon="chat"]'

    browser.get(Link)
    browser.maximize_window()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, chat)))
    print("QR scanned")

def send_message(target):
    global message,wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        group_title.click()
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
        time.sleep(1)
    except NoSuchElementException:
        return

def send_unsaved_contact_message():
    global message
    try:
        indicator = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
        wait.until(EC.presence_of_element_located((By.XPATH, indicator)))

        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
    except NoSuchElementException:
        print("Failed to send message")
        return

def send_attachment():
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    time.sleep(3)

    hour = datetime.datetime.now().hour

    # After 5am and before 11am scheduled this.
    if(hour >=5 and hour <=11):
        image_path = os.getcwd() +"\\Media\\" + 'goodmorning.jpg'
    # After 9pm and before 11pm schedule this
    elif (hour>=21 and hour<=23):
        image_path = os.getcwd() +"\\Media\\" + 'goodnight.jpg'
    else: # At any other time schedule this.
        image_path = os.getcwd() +"\\Media\\" + 'howareyou.jpg'
    # print(image_path)

    autoit.control_focus("Open","Edit1")
    autoit.control_set_text("Open","Edit1",(image_path) )
    autoit.control_click("Open","Button1")

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()

#Function to send Documents(PDF, Word file, PPT, etc.)
def send_files():
    global doc_filename
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send a Document(PDF, Word file, PPT)
    docButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    time.sleep(1)

    docPath = os.getcwd() + "\\Documents\\" + doc_filename

    autoit.control_focus("Open","Edit1")
    autoit.control_set_text("Open","Edit1",(docPath) )
    autoit.control_click("Open","Button1")

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()


def sender():
    global Contact,choice, docChoice, unsaved_Contacts
    Contact = []
    for i in Contact:
        send_message(i)
        print("Message sent to ",i)
        if(choice=="yes"):
            try:
                send_attachment()
            except:
                print('Attachment not sent.')
        if(docChoice == "yes"):
            try:
                send_files()
            except:
                print('Files not sent')

    if len(unsaved_Contacts)>0:
        for number in unsaved_Contacts:
            #driver  = webdriver.Chrome()
            link = "https://web.whatsapp.com/send?phone="+number
            print(link)
            browser.get(link)
            #browser.find_element_by_xpath('//*[@id="action-button"]').click()

            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.copyable-area')))
            print("Sending message to", number)
            send_unsaved_contact_message()

            #img_path = os.getcwd() +"\\Media\\" + 'enviar.jpg'
            img_path = os.getcwd() +"/Media/" + 'enviar.jpg'

            # To send attachments

            indicator_messagable = 'span[data-icon="clip"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, indicator_messagable)))
            # click to add
            browser.find_element_by_css_selector('span[data-icon="clip"]').click()

            # add file to send by file path
            browser.find_element_by_css_selector('input[type="file"]').send_keys(img_path)

            indicator_uploaded = 'span[data-icon="send-light"]'
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, indicator_uploaded)))
            # click to send
            browser.find_element_by_css_selector('span[data-icon="send-light"]').click()

            if(choice=="yes"):
                try:
                    send_attachment()
                except:
                    print('Attachment not sent.')
            if(docChoice == "yes"):
                try:
                    send_files()
                except:
                    print('Files not sent')
            time.sleep(7)

if __name__ == "__main__":
    global unsaved_Contacts
    print("Bienvenido")

    # Append more contact as input to send messages
    #input_contacts()

    # Lista de contactos
    unsaved_Contacts = []

    with open('input.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            unsaved_Contacts.append(row[0])

    # Enter the message you want to send
    input_message()

    #Enviar adjuntos Imagen/Video
    #choice = input("Desea enviar adjuntos?(yes/no): ")

    #docChoice = input("Would you file to send a Document file(yes/no): ")
    #if(docChoice == "yes"):
        # Note the document file should be present in the Document Folder
        #doc_filename = input("Enter the Document file name you want to send: ")

    # Logearse y escanear
    print("SCANEE SU CODIGO QR EN WHATSAPP WEB")
    whatsapp_login()

    sender()

    print("Tarea completada")

    browser.quit()
