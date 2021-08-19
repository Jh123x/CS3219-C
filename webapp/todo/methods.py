from ..models import TodoItems, db
from flask import flash, request, redirect


def todo_delete():
    print(request.data)
    flash("delete API is working")
    return redirect('/')

def todo_put():
    print(request.data)
    flash("put API is working")
    return redirect('/')

def todo_post():
    print(request.__dict__)
    name = request.form.get('name')
    details = request.form.get("details", "")
    is_complete = request.form.get("is_complete", False)
    new_item = TodoItems(name=name, details=details, is_complete=is_complete)

    # Add the item and commit
    db.session.add(new_item)
    db.session.commit()

    flash(f"Added {new_item.name} to list")
    return redirect('/')