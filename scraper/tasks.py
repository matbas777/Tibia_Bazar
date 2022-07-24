from Tibia_Market.celery import app

@app.task()
def test_task():
    print('ping')

@app.task()
def get_links():
    from scraper_links import get_all_pages_links
    get_all_pages_links()

@app.task()
def collect_data():
    from scraper_character import collect_data
    collect_data()