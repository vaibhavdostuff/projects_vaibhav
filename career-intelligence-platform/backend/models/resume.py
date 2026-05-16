from app import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    resume_text = db.Column(db.Text)
    predicted_role = db.Column(db.String(100))
    ats_score = db.Column(db.Integer)