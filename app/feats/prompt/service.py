from fastapi import HTTPException
from openai import OpenAI, AsyncOpenAI

from app.feats.embedding.service import retrieve_similar_documents
from app.feats.mentors.schemas import MentorDTO
from app.feats.mentors.service import update_current_action_result, insert_new_action, \
    update_curriculum, update_complete_current_action, update_curriculum_phase, update_giveup_current_action
from app.feats.moderation.service import check_moderation_violation, check_moderation_violation_async
from app.feats.prompt.const import *
from app.feats.prompt.schemas import CurriculumRequest
from app.feats.prompt.utils import extract_tagged_sections, inject_variables
from app.settings import settings

OPENAI_MODEL = settings.gpt_model
OPENAI_EMBEDDING_MODEL = settings.gpt_embedding_model

"""
Curriculum
"""


async def ask_curriculum_async(client: AsyncOpenAI,
                               mentor: MentorDTO,
                               curriculum_request: CurriculumRequest
                               ):
    is_violation = await check_moderation_violation_async(curriculum_request.hint, client)
    if is_violation:
        raise HTTPException(status_code=400, detail="다시 시도해주세요. 입력하신 내용에 부적절한 내용이 포함되어 있습니다.")

    variables = {
        "FIELD": mentor.get_field_to_str(),
        "STICC": mentor.get_STICC_to_str(),
        "HINT": curriculum_request.hint,
    }
    formatted_prompt = inject_variables(prompt_curriculum, variables)
    response = await client.chat.completions.create(
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


async def save_curriculum(db, mentor: MentorDTO, curriculum: str):
    return await update_curriculum(db, mentor.mentor_id, curriculum)


"""
Action
"""


async def suggest_actions_async(client: AsyncOpenAI, mentor: MentorDTO, hint: str):
    variables = {
        "STICC": mentor.get_STICC_to_str(),
        "FIELD": mentor.get_field_to_str(),
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
    }
    formatted_prompt = inject_variables(prompt_suggest_three_action, variables)

    response = await client.chat.completions.create(
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


async def make_current_action(client: AsyncOpenAI, db, mentor: MentorDTO, action: str):
    # TODO: Check if action is valid using openai
    await update_current_action_result(db, mentor.mentor_id, is_active=False, is_done=False)
    return await insert_new_action(db, mentor.mentor_id, action, is_active=True, is_done=False)


async def complete_action_async(client: AsyncOpenAI, db, mentor: MentorDTO, action: str, comment: str):
    is_violation = await check_moderation_violation_async(comment, client)
    if is_violation:
        raise HTTPException(status_code=400, detail="다시 시도해주세요. 입력하신 내용에 부적절한 내용이 포함되어 있습니다.")

    variables = {
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
        "FIELD": mentor.get_field_to_str(),
        "STICC": mentor.get_STICC_to_str(),
        "ACTION": action,
        "COMMENT": comment
    }
    formatted_prompt = inject_variables(prompt_complete_action, variables)
    response = await client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.70,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.65,
    )
    response_content = response.choices[0].message.content.strip()
    parsed_response = extract_tagged_sections(response_content)

    phase = parsed_response["UPDATED_PHASE"]
    phase = phase if phase else mentor.get_curr_phase()

    feedback = parsed_response["FEEDBACK"]
    feedback = feedback if feedback else "No feedback provided."

    # Update current action
    await update_complete_current_action(db, mentor.mentor_id, feedback)

    # Update mentor's phase
    await update_curriculum_phase(db, mentor.mentor_id, phase)

    return parsed_response


async def giveup_action_async(client, db, mentor: MentorDTO, action: str, comment: str):
    is_violation = await check_moderation_violation_async(comment, client)
    if is_violation:
        raise HTTPException(status_code=400, detail="다시 시도해주세요. 입력하신 내용에 부적절한 내용이 포함되어 있습니다.")

    variables = {
        "FIELD": mentor.get_field_to_str(),
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
        "STICC": mentor.get_STICC_to_str(),
        "ACTION": action,
        "REASON": comment
    }
    formatted_prompt = inject_variables(prompt_giveup_action, variables)
    response = await client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.70,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.65,
    )
    response_content = response.choices[0].message.content.strip()
    parsed_response = extract_tagged_sections(response_content)

    phase = parsed_response["UPDATED_PHASE"]
    phase = phase if phase else mentor.get_curr_phase()

    feedback = parsed_response["FEEDBACK"]
    feedback = feedback if feedback else "No feedback provided."

    # Update current action
    await update_giveup_current_action(db, mentor.mentor_id, feedback)

    # Update mentor's phase
    await update_curriculum_phase(db, mentor.mentor_id, phase)

    return parsed_response


"""
Question
"""


async def ask_question_async(client, mentor: MentorDTO, user_question: str, document_excerpts: str = "No document excerpts available."):
    is_violation = await check_moderation_violation_async(user_question, client)
    if is_violation:
        raise HTTPException(status_code=400, detail="다시 시도해주세요. 입력하신 내용에 부적절한 내용이 포함되어 있습니다.")

    variables = {
        "FIELD": mentor.get_field_to_str(),
        "CURRICULUM": mentor.get_curriculum(),
        "PHASE": mentor.get_curr_phase(),
        "STICC": mentor.get_STICC_to_str(),
        "QUESTION": user_question,
        "DOCUMENT_EXCERPTS": document_excerpts
    }
    formatted_prompt = inject_variables(prompt_question, variables)
    response = await client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": f"Your name is {mentor.mentor_name}." + formatted_prompt + prompt_always_korean
            },
        ],
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.5,
    )
    response_content = response.choices[0].message.content.strip()
    return extract_tagged_sections(response_content)
