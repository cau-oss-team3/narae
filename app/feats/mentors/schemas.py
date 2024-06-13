from enum import Enum

from pydantic import field_validator, BaseModel, Field

from app.core.exceptions import AuthenticationFailedException

MIN_LENGTH = 1
MAX_LENGTH = 256


# make EnumActionStatus in Enum - completed, not_completed, all
class ActionStatus(str, Enum):
    all = "all"
    done = "done"
    current = "current"


class STICC(BaseModel):
    situation: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    task: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    intent: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    concern: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    calibrate: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)

    def get_STICC_to_str(self):
        return (f"Situation: {self.situation}\n"
                f"Task: {self.task}\n"
                f"Intent: {self.intent}\n"
                f"Concern: {self.concern}\n"
                f"Calibrate: {self.calibrate}")

    # token length 제한
    @field_validator("situation", mode="before")
    @classmethod
    def validate_situation_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("task", mode="before")
    @classmethod
    def validate_task_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("intent", mode="before")
    @classmethod
    def validate_intent_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("concern", mode="before")
    @classmethod
    def validate_concern_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("calibrate", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v


class CreateMentorDTO(BaseModel):
    mentor_name: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    mentor_field: int = Field(ge=0, le=2)
    mentor_sticc: STICC

    @field_validator("mentor_name", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > 45:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 1:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v


class MentorDTO(BaseModel):
    mentor_id: int
    mentor_name: str = Field(min_length=1, max_length=45)
    mentor_field: int = Field(ge=0, le=2)
    mentor_sticc: STICC
    curriculum: str = ""
    curriculum_phase: str = ""

    @field_validator("mentor_name", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > 45:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 1:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    def get_STICC_to_str(self):
        return self.mentor_sticc.get_STICC_to_str()

    def get_field_to_str(self):
        if self.mentor_field == 0:
            return "Backend"
        elif self.mentor_field == 1:
            return "Frontend"
        elif self.mentor_field == 2:
            return "Fullstack"

    def get_curriculum(self):
        if self.curriculum is None or self.curriculum == "":
            return "Not set"
        return self.curriculum

    def get_curr_phase(self):
        if self.curriculum_phase is None or self.curriculum_phase == "":
            return "Not set"
        return self.curriculum_phase
