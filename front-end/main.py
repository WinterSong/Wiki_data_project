#!/usr/bin/env python
#coding:utf-8

import web
from querys import querys

class index:
	def GET(self):
		return render.index()

	def POST(self):
		instance = querys()
		form = web.input()
		if form.get("select")=="entity":
			try:
				name = form.get("input")
				ids,dsc = instance.query1(name)
				instance.final()
				return render.search(ids,dsc,name)
			except:
				return render.error()
		else:
			try:
				name = form.get("input")
				result = instance.query5(name)
				instance.final()
				return render.detail(result[0],result[1],result[2])
			except:
				return render.error()

class search:
	def POST(self):
		try:
			form = web.input()
			return render.search()
		except:
			return render.error()

class detail:
	"""detail property for entity"""
	def GET(self):
		try:
			instance = querys()
			entityId = web.input().get('entity')
			info,aliases,properties = instance.query4(entityId)

			instance.final()
			return render.detail(info,aliases,properties)
		except:
			return render.error()

class error:
	def GET(self):
		return render.error()
render = web.template.render('templates/')
urls = (
	'/',index,
	'/search',search,
	'/detail',detail,
	'/error',error
	)

app = web.application(urls, globals(), autoreload=True)



if __name__ == '__main__':
	app.run()