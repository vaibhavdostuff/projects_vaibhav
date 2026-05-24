def calculate_ats(skills_count, formatting, experience):

    score = (
        skills_count * 5 +
        formatting * 20 +
        experience * 15
    )

    return min(score, 100)