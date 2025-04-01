from flask import Blueprint, url_for
from flask_babel import lazy_gettext as _

from bridg import Person
from bridg.common.person import TelecommunicationAddress
from web.db import db
from web.views import BreadcrumbsMixin, ContextMixin, CreateView, DeleteView, EditView, HTMXDeleteMixin, SQLAlchemyMixin

from .form import TelecomForm

blueprint = Blueprint("telecom_address", __name__,
                      url_prefix="/telecom_address")


class PersonMixin(ContextMixin, SQLAlchemyMixin):
    def setup(self, person_id: int, **kwargs):
        self.person = db.session.query(Person).filter_by(id=person_id).one()
        super().setup(person_id=person_id, **kwargs)

    def get_context(self):
        ctx = super().get_context()
        ctx["person"] = self.person
        return ctx


class TelecomCreateView(PersonMixin, BreadcrumbsMixin, CreateView):
    db = db
    model = TelecommunicationAddress
    form_class = TelecomForm
    template_name = "person/telecom_address/edit.html"

    def get_data(self, form, person_id, scheme, **kwargs):
        data = super().get_data(form, person_id=person_id, scheme=scheme, **kwargs)
        data["person_id"] = person_id
        data["scheme"] = scheme
        return data

    def url_for_redirect(self, person_id, **kwargs):
        return url_for("person.show", id=person_id)

    def setup_breadcrumbs(self, person_id, **kwargs):
        self.add_breadcrumb(None, _("Persons"))
        self.add_breadcrumb("person.show", str(self.person), id=person_id)
        self.add_breadcrumb(".new", _("Add telecom address"))


class TelecomEditView(PersonMixin, BreadcrumbsMixin, EditView):
    db = db
    model = TelecommunicationAddress
    form_class = TelecomForm
    template_name = "person/telecom_address/edit.html"

    def url_for_redirect(self, person_id, **kwargs):
        return url_for("person.show", id=person_id)

    def setup_breadcrumbs(self, person_id, **kwargs):
        self.add_breadcrumb(None, _("Persons"))
        self.add_breadcrumb("person.show", str(
            self.object.person_id), id=person_id)
        self.add_breadcrumb("person.edit", _("Edit"))


class TelecomFormDeleteView(HTMXDeleteMixin, DeleteView):
    db = db
    model = TelecommunicationAddress

    def url_for_redirect(self, person_id, **kwargs):
        return url_for("person.show", id=person_id)


blueprint.add_url_rule("/new", view_func=TelecomCreateView.as_view("new"))
blueprint.add_url_rule("/<id>/edit", view_func=TelecomEditView.as_view("edit"))
blueprint.add_url_rule(
    "/<id>", view_func=TelecomFormDeleteView.as_view("delete"))
