from BaseTest import BaseTest

class TestMainController(BaseTest):

	def test_404(self):
		rv = self.app.get("/non-existant-url")
		assert rv.status == self.notFound

	def test_main(self):
		rv = self.app.get("/")
		assert rv.status == self.ok

	def test_rules(self):
		rv = self.app.get("/rules")
		assert rv.status == self.ok

	def test_favicon(self):
		rv = self.app.get("/favicon.ico")
		assert rv.status == self.ok