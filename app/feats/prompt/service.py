from app.feats.prompt.const import *
from app.feats.prompt.schemas import CurriculumRequest
from app.feats.prompt.utils import extract_tagged_sections, inject_variables
from app.settings import settings
from app.feats.mentors.schemas import MentorDTO

OPENAI_MODEL = settings.gpt_model
OPENAI_EMBEDDING_MODEL = settings.gpt_embedding_model

"""
Curriculum
"""


def ask_curriculum(client,
                   mentor: MentorDTO,
                   curriculum_request: CurriculumRequest):
    formatted_prompt = inject_variables(prompt_curriculum,
                                        {
                                            "FIELD": mentor.get_field_to_str(),
                                            "STICC": mentor.get_STICC_to_str(),
                                            "HINT": curriculum_request.hint,
                                        })

    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.75,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    response_content = response.choices[0].message.content.strip()
    return extract_tagged_sections(response_content)


"""
Action
"""


def ask_actions(client, mentor: MentorDTO):
    variables = {
        "STICC": mentor.get_STICC_to_str(),
        "FIELD": mentor.get_field_to_str(),
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
    }
    formatted_prompt = inject_variables(prompt_suggest_three_action, variables)

    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.75,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    response_content = response.choices[0].message.content.strip()
    return extract_tagged_sections(response_content)


def accept_action(client, mentor: MentorDTO, user_situation: str):
    ...


def giveup_action(client, mentor: MentorDTO, user_situation: str):
    ...


"""
Question
"""


def ask_question(client, mentor: MentorDTO, user_question: str):
    variables = {
        "FIELD": mentor.get_field_to_str(),
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
        "STICC": mentor.get_STICC_to_str(),
        "QUESTION": user_question,
    }
    formatted_prompt = inject_variables(prompt_question, variables)
    print(formatted_prompt)

    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.5,
    )
    response_content = response.choices[0].message.content.strip()
    return extract_tagged_sections(response_content)


"""
Will be deprecated
"""


def legacy_action(abandon_reason, client, existing_learning, learning_goal, recommend_action):
    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the next action which depends to the today's study "
                           "direction. Your message is given to the user after the's study direction is given. Make "
                           "sure your advice is specific enough to be actionable and at the right level of difficulty."
                           "Also, make sure to motivate the user to keep going."
                           "If the user completes the action, please provide feedback on how they completed it."
                           "If the user abandons the action, ask for the reason and suggest the next recommended "
                           "action based on the reason."
                           f"Existing learning content: {existing_learning}\n"
                           f"Learning goal: {learning_goal}\n"
                           "Please recommend an action that can be done according to today's learning direction.",
            },
            {
                "role": "user",
                "content": recommend_action.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )

    # 사용자가 액션을 완료할 시 이에 대한 응답
    response_text = response.choices[0].message.content.strip()
    if "completed" in response_text.lower():
        feedback_prompt = "Please provide feedback on how you completed the action."
        response_with_feedback = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": feedback_prompt,
                },
                {
                    "role": "user",
                    "content": response_text,
                },
            ],
            temperature=0.5,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text += (
                "\n\nFeedback: " + response_with_feedback.choices[0].message.content.strip()
        )

    # 사용자가 액션을 포기할 시 이에 대한 응답
    elif "abandoned" in response_text.lower():
        reason_prompt = "Please specify the reason for abandoning the action."
        next_action_prompt = "Based on your reason for abandoning the action, here's the next recommended action."

        reason_response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": reason_prompt,
                },
                {
                    "role": "user",
                    "content": abandon_reason,
                },
            ],
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        next_action_response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": next_action_prompt,
                },
                {
                    "role": "user",
                    "content": reason_response.choices[0].message.content.strip(),
                },
            ],
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        response_text += (
            f"\n\nReason for abandoning: {reason_response.choices[0].message.content.strip()}"
            f"\n\nNext recommended action: {next_action_response.choices[0].message.content.strip()}"
        )
    return response_text
