import datetime

from playwright.sync_api import Page, expect

from bridg import AdministrativeGender, Person
from web.db import db


def test_person_show(app, server, page: Page):
    url = app.url_for("person.show", id='1')
    request = page.request.get(url)
    expect(request).to_be_ok()


def test_person_edit(app, server, page: Page):
    url = app.url_for("person.edit", id='1')
    request = page.request.get(url)
    expect(request).to_be_ok()


def test_edit(app, server, page: Page):
    src = {'id': 7, 'administrative_gender_code': AdministrativeGender.male,
           'death_indicator': False, 'birth_date': datetime.date(1991, 1, 1)}
    url = app.url_for("person.edit", id=src['id'])
    page.goto(url)
    page.locator("id=administrative_gender_code").select_option(
        src['administrative_gender_code'].value)
    page.locator("id=death_indicator").select_option(
        str(src['death_indicator']).lower())
    page.locator("id=birth_date").fill(src['birth_date'].strftime('%Y-%m-%d'))
    page.get_by_text("Save").all()[1].click()
    with app.app_context():
        result = db.session.query(Person).filter_by(id=src['id']).one()
        res = {'id': result.id, 'administrative_gender_code': result.administrative_gender_code,
               'death_indicator': result.death_indicator, 'birth_date': result.birth_date}
        assert res == src
