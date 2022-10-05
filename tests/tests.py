from app.blueprints.page.models.widget import Widget


def test_create_widget() -> Widget:
    widget: Widget = Widget(**{'name': "Ricky", 'number_of_parts': 35})

    assert(widget is not None)
    assert(widget.name == 'Ricky')
    assert(widget.number_of_parts == 35)

    return widget


def test_delete_widget():
    widget: Widget = test_create_widget()

    assert(widget is not None)
    widget.save()

    w: Widget = Widget.query.filter(Widget.id == widget.id).scalar()
    assert(w is not None)

    w_id = w.id

    w.delete()
    w = Widget.query.filter(Widget.id == w_id).scalar()
    assert(w is None)
