from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
       
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0  

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]  

    
    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
   
    try:
        if current_question_id is None:
            return False, "No active question to answer."

        current_question = PYTHON_QUESTION_LIST[current_question_id]
        valid_answers = current_question.get("valid_answers", [])

        if answer.lower() not in [ans.lower() for ans in valid_answers]:
            return False, "Invalid answer. Please try again."

        if "answers" not in session:
            session["answers"] = {}
        session["answers"][current_question_id] = answer
        return True, ""
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


def get_next_question(current_question_id):
   
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]["question"]
        return next_question, next_question_id
    return None, None 


def generate_final_response(session):
    try:
        answers = session.get("answers", {})
        score = 0

        for question_id, user_answer in answers.items():
            correct_answers = PYTHON_QUESTION_LIST[question_id].get("valid_answers", [])
            if user_answer.lower() in [ans.lower() for ans in correct_answers]:
                score += 1

        total_questions = len(PYTHON_QUESTION_LIST)
        return f"Thank you for completing the quiz! Your score is {score}/{total_questions}."
    except Exception as e:
        return f"An error occurred while calculating your result: {str(e)}"
