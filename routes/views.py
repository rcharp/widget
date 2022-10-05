import names
import random
from flask import Blueprint, render_template, flash
from app.extensions import csrf, db
from flask import redirect, url_for, request
from flask_cors import cross_origin
from app.blueprints.page.models.widget import Widget

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/', methods=['GET'])
@cross_origin()
def home():
    all_widgets: list = get_widgets()
    widgets: list = all_widgets[:10]
    return render_template('page/app.html', widgets=widgets, widget_length=len(all_widgets))


@page.route('/create', methods=['POST'])
@page.route('/create/<rand>', methods=['POST'])
@csrf.exempt
@cross_origin()
def create(rand=False):
    if request.method == 'POST':
        data = {
            'name': names.get_full_name(),
            'number_of_parts': random.randint(1, 100)
        } if rand else {
            'name': request.form.get('name'),
            'number_of_parts': request.form.get('number-parts')
        }

        w: Widget = Widget(**data)
        w.save()
        flash('Successfully created widget!', 'success')

    return redirect(url_for('page.home'))


@page.route('/read/<int:widget_id>', methods=['GET'])
@csrf.exempt
@cross_origin()
def read(widget_id):
    w: Widget = Widget.query.filter(Widget.id == widget_id).scalar()
    if not w:
        flash('Could not find that widget. Please try again!', 'danger')
        return redirect(url_for('page.home'))

    return render_template('page/widget.html', widget=w)


@page.route('/list', methods=['GET'])
@csrf.exempt
@cross_origin()
def list_widgets():
    widgets: list = get_widgets()
    return render_template('page/all.html', widgets=widgets, widget_length=len(widgets))


@page.route('/update/<int:widget_id>', methods=['POST'])
@csrf.exempt
@cross_origin()
def update(widget_id):
    try:
        data = {
            'name': request.form.get('name'),
            'number_of_parts': request.form.get('number-parts')
        }
        db.session.query(Widget).filter(Widget.id == widget_id).update(data)
        db.session.commit()
        db.session.flush()

        flash('Successfully updated widget!', 'success')
    except Exception:
        flash('There was an error updating this widget. Please try again.', 'danger')
    return redirect(url_for('page.home'))


@page.route('/delete/<int:widget_id>', methods=['GET'])
@csrf.exempt
@cross_origin()
def delete(widget_id):
    w: Widget = Widget.query.filter(Widget.id == widget_id).scalar()
    if w is None:
        flash('There was an error deleting this widget. Please try again.', 'danger')
    else:
        w.delete()
        flash('Successfully deleted this widget.', 'success')
    return redirect(url_for('page.home'))


def get_widgets() -> list:
    return Widget.query.order_by(Widget.updated_on.desc()).all()
