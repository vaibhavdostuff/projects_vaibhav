from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')


def generate_questions(role):

    prompt = f'''
    Generate 20 interview questions for {role}
    '''

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content