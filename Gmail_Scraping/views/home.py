from app.common.helpers import *

from flask import render_template, redirect, url_for
from flask.views import MethodView
from flask_restful import Resource, reqparse, current_app


class Home(MethodView):
	def get(self):
		
		cur = g.db.query(
			""" SELECT	
					*
				FROM campaign_has_reports
				LIMIT 100""")
		
		for r in list(cur):
			print(r)


		
		return render_template('index.html', data={})
