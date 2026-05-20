from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')


def generate_roadmap(skills, role):

    prompt = f'''
    User skills: {skills}
    Target Role: {role}

    Generate 6 month learning roadmap.
    '''

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content