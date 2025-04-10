from playwright.sync_api import Page
from toolz import dissoc

from bridg import converter
from bridg.common.person import TelecommunicationAddress
from web.db import db


def test_telecom_edit(app, server, page: Page):
    src = {'use': None, 'address': '+1-214-559-6993',
           'id': 11, 'person_id': 7, 'scheme': 'tel'}
    with app.app_context():
        telecom = TelecommunicationAddress(use=src['use'], address=src['address'],
                                           id=src['id'], person_id=src['person_id'], scheme=src['scheme'])
        db.session.add(telecom)
        db.session.commit()
        url = app.url_for("person.telecom_address.edit", person_id=7, id=2)
        page.goto(url)
        page.locator("id=address").fill(src['address'])
        form = page.locator('#person-telecom-form')
        submit = form.locator('[type ="submit"]')
        submit.click()
        result = db.session.query(
            TelecommunicationAddress).filter_by(person_id=7).one()
        res = converter.unstructure(result)
        db.session.delete(result)
        db.session.commit()
        assert src == res


def test_telecom_new(app, server, page: Page):
    src = {'use': None, 'address': '+1-214-559-6993',
           'person_id': 7, 'scheme': 'tel'}
    url = app.url_for("person.telecom_address.new",
                      person_id=src['person_id'], scheme=src['scheme'])
    page.goto(url)
    page.locator("id=address").fill(src['address'])
    form = page.locator('#person-telecom-form')
    submit = form.locator('[type ="submit"]')
    submit.click()
    with app.app_context():
        result = db.session.query(
            TelecommunicationAddress).filter_by(person_id=src['person_id']).one()
        res = dissoc(converter.unstructure(result), 'id')
        db.session.delete(result)
        db.session.commit()
        assert src == res


def test_telecom_delete(app, server, page: Page):
    src = {'use': None, 'address': '+1-214-559-6993',
           'id': 10, 'person_id': 7, 'scheme': 'tel'}
    with app.app_context():
        telecom = TelecommunicationAddress(use=src['use'],
                                           address=src['address'],
                                           id=src['id'],
                                           person_id=src['person_id'],
                                           scheme=src['scheme'])
        db.session.add(telecom)
        db.session.commit()
        url = app.url_for("person.telecom_address.edit",
                          person_id=src['person_id'], id=src['id'])
        page.goto(url)
        page.locator('#actions').click()
        page.locator('#delete').click()
        page.wait_for_url(app.url_for("person.show", id=src['person_id']))
        result = db.session.query(
            TelecommunicationAddress).filter_by(id=src['id']).all()
        assert not result
