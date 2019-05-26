from django.core.management import BaseCommand
from app_api.crawler import crawler

# A classe deve ter o nome Command, e herdar de BaseCommand
class Command(BaseCommand):
	# Exibe isso quando usuario digitar help (manage.py coletar_leituras help)
	help = "Sistema automatizado de coleta das cotações"

	# Um command deve definir um handle()
	def handle(self, *args, **options):
		crawler.crawler()
