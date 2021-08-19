from ..models import TodoItems, db
from flask import flash, request, redirect, Response


def todo_delete():
    id = request.form.get('id')
    item = TodoItems.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    flash(f"{item.name} is deleted")    
    return Response(status=204)

def todo_put():
    id = request.form.get('id')
    item = TodoItems.query.filter_by(id=id).first()
    item.is_complete = True
    db.session.commit()
    flash(f"{item.name} is completed")
    return Response(status=204)

def todo_post():
    name = request.form.get('name')
    details = request.form.get("details", "")
    is_complete = request.form.get("is_complete", False)
    new_item = TodoItems(name=name, details=details, is_complete=is_complete)

    # Add the item and commit
    db.session.add(new_item)
    db.session.commit()

    flash(f"Added {new_item.name} to list")
    return redirect('/')