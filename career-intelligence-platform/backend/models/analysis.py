from app import db

class Analysis(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    ats_score = db.Column(
        db.Integer
    )

    predicted_role = db.Column(
        db.String(100)
    )

    extracted_skills = db.Column(
        db.Text
    )

    recommendations = db.Column(
        db.Text
    )