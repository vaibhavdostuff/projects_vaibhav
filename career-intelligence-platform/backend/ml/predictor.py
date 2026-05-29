import joblib

model = joblib.load(
    'ml/career_model.pkl'
)

def predict_role(resume_text):

    prediction = model.predict(
        [resume_text]
    )[0]

    return prediction