from flask import current_app as app
from flask_mail import Mail
from flask_mail import Message
from pingpong.app import app as context
from pingpong.decorators.Async import async
from pingpong.services.OfficeService import OfficeService
import requests
import json
import threading

officeService = OfficeService()

def getRecipients(officeIds):
	recipients = []

	if isinstance(officeIds, list):
		offices = officeService.selectByIds(officeIds)
		for office in offices:
			if office.hasSkypeChatId():
				recipients.append(office.skypeChatId)

	else:
		office = officeService.selectById(officeIds)
		recipients.append(office.skypeChatId)

	return recipients

def mailError( message):
	app.logger.info("Sending Error Email...")

	subject = "Ping Pong App ERROR"
	body = "Ping Pong App ERROR\nMessage: {}".format(message)
	html = "<h2>Ping Pong App ERROR</h2><p>Message: {}".format(message)
	mail(subject, body, html)

def mailFeedback(name, email, message):
	app.logger.info("Sending Feedback...")

	subject = "Ping Pong App Feedback"
	body = "Ping Pong App Feedback\nName: {}\nEmail: {}\n\n{}".format(name, email, message)
	html = "<h2>Ping Pong App Feedback</h2><p>Name: {}<br />Email: {}<p><p>{}</p>".format(name, email, message)
	mail(subject, body, html)

def send(message):
	app.logger.info("Teams message being sent %s", message)
	url = app.config["TEAMS_WEBHOOK_URL"]
	doSend(url, message)

def mail(subject, body, html):
	sender = (app.config["MAIL_FROM_NAME"], app.config["MAIL_FROM_EMAIL"])
	recipients = app.config["MAIL_RECIPIENTS"]

	app.logger.info("\
		Sending Mail...\n\
		FROM: %s\n\
		TO: %s\n\
		SUBJECT: %s\n\
		BODY: %s\n\
		HTML: %s\
	", sender, recipients, subject, body, html)

	mail = Mail(app)
	messages = Message(subject, sender = sender, recipients = recipients)
	messages.body = body
	messages.html = html

	doMail(mail, messages)

@async
def doSend(url, message):

	headers = { "Content-Type" : "application/json" }

	data = {
		"@type": "MessageCard",
		"@context": "http://schema.org/extensions",
		"text": message,
		"themeColor": "E81123",
	}

	data = json.dumps(data)

	requests.post(url, data = data, headers = headers)

@async
def doMail(mail, messages):
	with context.app_context():
		mail.send(messages)
