#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
	<title>User Signup</title>
	<style>
		.error {
			color: red;
			font-family: Courier;
		}

		h1 {
			background-color: black;
			color: white;
			width: 110px;
			font-family: Helvetica;
			padding: 7px;
		}

		label {
			background-color: #444;
			color: white;
			padding: 2px 7px 2px 5px;
			font-family: Helvetica;
		}
	</style>
</head>
"""



class MainHandler(webapp2.RequestHandler):

	header = "<h1>Signup</h1>"

	form = """<form action="/" method="post">
		<label>Username:</label>
		<input type="text" name="username" value="%(username)s">
		<span class="error">%(username_error)s</span>
		<br>
		
		<label>Password:</label>
		<input type="Password" name="password">
		<br>

		<label>Verify Password:</label>
		<input type="password" name="verify">
		<span class="error">%(password_error)s</span>
		<br>

		<label>Email (optional):</label>
		<input type="text" name="email" value="%(email)s">
		<span class="error">%(email_error)s</span>
		<br><br>

		<input type="submit" value="submit">
	</form>"""

	def write_form(self, username="", email="", username_error="", password_error="", email_error=""):
		self.response.out.write(page_header + self.header + self.form % {'username_error': username_error,
																		 'password_error': password_error,
																		 'email_error': email_error,
																		 'username': username,
																		 'email': email})

	def get(self):
		#send the plain form to the browser using the response object
		self.write_form()

	def post(self):
		user_username = self.request.get("username")
		user_password = self.request.get("password")
		user_verify = self.request.get("verify")
		user_email = self.request.get("email")

		#username validation-----
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		def valid_username(username):
			return USER_RE.match(user_username)

		#username variable will either be MATCH or NONE, not the actual user_username
		username = valid_username(user_username)
		if not username:
			username_error = "Invalid Username"
		else:
			username_error = ""
			
		
		#password validation-----
		password = ""	
		if user_password != user_verify:
			password_error = "Passwords must match"
		else:
			PASS_RE = re.compile(r"^.{3,20}$")
			def valid_password(password):
				return PASS_RE.match(user_password)

			password = valid_password(user_password)
			if not password:
				password_error = "Invalid password"	
			else:
				password_error = ""

	
		#email validation-----
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		def valid_email(email):
			return EMAIL_RE.match(user_email)

		email = ""
		email_error = ""
		#if user entered an email	
		if user_email:
			#validate the email
			email = valid_email(user_email)
			#if email is invalid:
			if not email:
				email_error = "Invalid email"
			#if email is valid
			else:
				email_error = ""
			#check all 3 fields
			if not (username and password and email):
				self.write_form(user_username, user_email, username_error, password_error, email_error)
			else:
				self.redirect("/welcome?username=" + user_username)

		#if the user did not enter an email
		else:
			#if user and password are invalid
			if not (username and password):
				#resend the form
				self.write_form(user_username, user_email, username_error, password_error, email_error)
			#if no email, and other fields are valid, redirect
			else:
				self.redirect("/welcome?username=" + user_username)
		

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		self.response.write("<h1>Welcome, {}!</h1>".format(username))



app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', WelcomeHandler)
], debug=True)
