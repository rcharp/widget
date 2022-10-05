from sqlalchemy import exists
import string
import random

from lib.util_sqlalchemy import ResourceMixin
from app.extensions import db


class Widget(ResourceMixin, db.Model):
    __tablename__ = 'widgets'

    # Objects.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    number_of_parts = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Widget, self).__init__(**kwargs)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def generate_id(cls, size=8):
        # Generate a random 8-character id
        chars = string.digits
        result = int(''.join(random.choice(chars) for _ in range(size)))

        # Check to make sure there isn't already that id in the database
        if not db.session.query(exists().where(cls.widget_id == result)).scalar():
            return result
        else:
            Widget.generate_id()

    @classmethod
    def bulk_delete(cls, ids):
        """
        Delete widgets in bulk

        :param ids: List of widget ids to be deleted
        :type ids: widget
        :return: int
        """
        delete_count = 0

        for id in ids:
            widget = Widget.query.get(id)

            if widget is None:
                continue

            widget.delete()

            delete_count += 1

        return delete_count
