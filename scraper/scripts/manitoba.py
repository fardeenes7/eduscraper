"""
University of Manitoba
https://umanitoba.ca/
"""

import re
import requests
from bs4 import BeautifulSoup
from scraper.models import University, Program


def stripdegree(string):
    degreelist = {
        "ma": "Master of Arts",
        "msc": "Master of Science",
        "meng": "Master of Engineering",
        "mfa": "Master of Fine Arts",
        "masc": "Master of Applied Science",
        "menv": "Master of Environment",
        "mfin": "Master of Finance",
        "mman": "Master of Management",
        "mmath": "Master of Mathematics",
        "mmed": "Master of Education",
        "mahn": "Master of Applied Human Nutrition",
        "march": "Master of Architecture",
        'med': "Master of Education",
        "phd": "Doctor of Philosophy",
        'other': 'Other',
    }
    #get only the text between parethesis
    try:
        string = re.search(r".*?\((.*?)\)", string).group(1)
        return string
    except:
        return "Other"

def get_programs():
    url = "https://umanitoba.ca/explore/programs-of-study/graduate"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    programs = []
    for program in soup.find("ol", class_="az-listing").find_all("a"):
        url = program.get("href")
        if url.startswith("/explore/"):
            url = "https://umanitoba.ca" + url
        if url.__contains__("explore"):
            programs.append(url)
    return programs


def get_program_details(program_url, university):
    page = requests.get(program_url)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        title = soup.find("span", class_="field--name-title").text
    except:
        try:
            title = soup.find("h1", class_="page-header__heading").text
        except:
            return
    degree = stripdegree(title)
    try:
        details = soup.find("section", id="program-details").find("div", class_="section__content")
    except:
        details=""

    try:
        duration=soup.find_all('div', class_='teaser__content')[2].find('p').text
    except:
        pass

    try:
        requirements = soup.find("section", id="admission-requirements").find("div", class_="section__content")
    except:
        requirements=""
    try:
        apply_instructions = soup.find("section", id="how-to-apply").find("div", class_="l-2col")
    except:
        apply_instructions=""

    try:
        contacts = soup.find("section", id="contact-us").find("div", class_="l-2col").find_all("div", class_='clearfix wysiwyg field field--name-body field--type-text-with-summary field--label-hidden field__item')
        # print(contacts)
        contact = ""
        for c in contacts:
            contact += str(c)
        
        
    except:
        contact=""

    try:
        program, created = Program.objects.get_or_create(title=title, university=university)
        program.url = program_url
        program.duration = duration
        program.details = str(details)
        program.requirements = str(requirements)
        program.apply_instructions = str(apply_instructions)
        program.degree = degree
        program.contact = str(contact)
        program.save()

    except Exception as e:
        print("Error saving ", title,": ", e)
        return

def scrape():
    print("Scraping University of Manitoba")
    university = University.objects.get(name="University of Manitoba")
    programs = get_programs()
    for program in programs:
        get_program_details(program, university)

    print("Done scraping University of Manitoba")
        