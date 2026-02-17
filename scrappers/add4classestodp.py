from dtp import db, app
from dtp.models import Class, Department
with app.app_context():
    departments = Department.query.all()

    for department in departments:
        for year in range(1, 5):
            new_class = Class(year=year, department_id=department.id)
            db.session.add(new_class)

    db.session.commit()
