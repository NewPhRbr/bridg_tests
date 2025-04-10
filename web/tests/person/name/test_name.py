from playwright.sync_api import Page, expect
from toolz import dissoc

from bridg import EntityName
from web.db import db


def test_person_showname(app, server, page: Page):
    url = app.url_for("person.name.edit", person_id=1, id=2)
    request = page.request.get(url)
    expect(request).to_be_ok()


def test_person_editname(app, server, page: Page):
    url = app.url_for("person.name.edit", person_id=1, id=2)
    request = page.request.get(url)
    expect(request).to_be_ok()


def test_person_editname_save(app, server, page: Page):
    src = {'id': 5, 'family': 'Trump',
           'given': 'Donald', 'middle': 'John', 'suffix': '',
           'patronymic': '', 'use': 'official', 'prefix': '',
           'biologic_entity_id': 7}
    url = app.url_for("person.name.edit", person_id=7, id=5)
    page.goto(url)
    page.locator("summary").click()
    page.locator("id=family").fill(src['family'])
    page.locator("id=given").fill(src['given'])
    page.locator("id=middle").fill(src['middle'])
    page.locator("id=suffix").fill(src['suffix'])
    form = page.locator('#person-name-form')
    submit = form.locator('[type ="submit"]')
    submit.click()
    with app.app_context():
        result = db.session.query(EntityName).filter_by(id=5).one()
        res = dissoc(result.__dict__, '_sa_instance_state')
        db.session.delete(result)
        db.session.commit()
        assert src == res


def test_person_name_delete(app, server, page: Page):
    src = {'id': 5, 'biologic_entity_id': 7}
    url = app.url_for("person.name.edit",
                      person_id=src['biologic_entity_id'], id=src['id'])
    with app.app_context():
        name = EntityName(id=src['id'],
                          biologic_entity_id=src['biologic_entity_id'])
        db.session.add(name)
        db.session.commit()
        page.goto(url)
        page.locator('#actions').click()
        page.locator('#delete').click()
        result = db.session.query(
            EntityName).filter_by(id=src['id']).all()

        assert not result
