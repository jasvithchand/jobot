
# jobot

A script that applies to a job posted on Workdays in one click.

![demo](https://github.com/user-attachments/assets/6053b061-b2ef-4f0a-8999-fb13da51bfd9)

## What it does

All the user information is stored in the userinfo.json file. It navigates through a series of web pages, and automagically fills out forms based on your predefined settings. It also creates the account if the account doent exist (Whew !). Why do it manually when you can do it automatically?

## Prerequisites

Note: I've added both the chrome and edge drivers to the repo so you dont have to (not accidental at all 🙃)

$ python3 -m pip install --upgrade pip

$ python3 -m pip install selenium
## How to Run

Add the job url's to the urls.json and we're good to go ! 

$ python3 jobot.py

## Notes

Several Workday job applications include additional required fields. If these aren't filled out, the submission might not go through, but don't worry—the code has a safety net! It will pause for 60 seconds, giving you a chance to manually correct any issues and hit Submit. Just remember, if these errors aren't fixed manually, the script will ultimately not succeed.

## Why though ?

I think majority might agree applying might be one of the most horrible experinces. Its a real pain in the a**. Unfortunatly, There are lot of tech gaint companies like NVDIA who are still using workday as their official job portal which is sad. Automating the job application process could save time and be incredibly beneficial in today’s competitive job market. 🧑🏽‍💻

## Enhancements
I cant wait to integrate this with an LLM to contextually analyse the info to identify the fields and generate answers based on the user data on the fly. 

### Thank you
Please feel free to use the code and suggest any modifications. Thank you.



