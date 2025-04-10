from playwright.sync_api import Page
from toolz import dissoc

from bridg import converter
from bridg.common.person import PostalAddress
from web.db import db


def test_postal_new(app, server, page: Page):
    src = {'use': None, 'person_id': 7, 'street': "", 'building': "",
           'country': "", 'municipality': "", 'state': "", 'zip': ""}
    url = app.url_for("person.postal_address.new", person_id=src['person_id'])
    page.goto(url)
    page.locator("#street").fill(src['street'])
    page.locator("#building").fill(src['building'])
    page.locator("#country").fill(src['country'])
    page.locator("#municipality").fill(src['municipality'])
    page.locator("#state").fill(src['state'])
    page.locator("#zip").fill(src['zip'])
    form = page.locator('#person-postal-form')
    submit = form.locator('[type ="submit"]')
    submit.click()
    with app.app_context():
        result = db.session.query(
            PostalAddress).filter_by(person_id=src['person_id']).one()
        res = dissoc(converter.unstructure(result), 'id')
        db.session.delete(result)
        db.session.commit()
        assert src == res


def test_postal_delete(app, server, page: Page):
    src = {'use': None, 'id': 5, 'person_id': 7, 'street': '',
           'building': '', 'country': '', 'municipality': '',
           'state': '', 'zip': ''}
    with app.app_context():
        postal = PostalAddress(id=src['id'],
                               person_id=src['person_id'])
        db.session.add(postal)
        db.session.commit()
        url = app.url_for("person.postal_address.edit",
                          person_id=src['person_id'], id=src['id'])
        page.goto(url)
        page.locator('#actions').click()
        page.locator('#delete').click()
        page.wait_for_url(app.url_for("person.show", id=src['person_id']))
        result = db.session.query(
            PostalAddress).filter_by(id=src['id']).all()
        assert not result


def test_postal_edit(app, server, page: Page):
    src = {'use': None, 'id': 5, 'person_id': 7, 'street': '',
           'building': '', 'country': '', 'municipality': '',
           'state': '', 'zip': ''}
    with app.app_context():
        postal = PostalAddress(id=src['id'], person_id=src['person_id'])
        db.session.add(postal)
        db.session.commit()
        url = app.url_for("person.postal_address.edit", person_id=7, id=5)
        page.goto(url)
        page.locator("#street").fill(src['street'])
        page.locator("#building").fill(src['building'])
        page.locator("#country").fill(src['country'])
        page.locator("#municipality").fill(src['municipality'])
        page.locator("#state").fill(src['state'])
        page.locator("#zip").fill(src['zip'])
        form = page.locator('#person-postal-form')
        submit = form.locator('[type ="submit"]')
        submit.click()
        result = db.session.query(
            PostalAddress).filter_by(person_id=7).one()
        res = converter.unstructure(result)
        db.session.delete(result)
        db.session.commit()
        assert src == res
