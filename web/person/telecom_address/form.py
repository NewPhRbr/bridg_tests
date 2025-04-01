from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import HiddenField, TelField


class TelecomForm(FlaskForm):
    address = TelField(_("Address"))
    scheme = HiddenField(_("Scheme"))
