from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .base import BaseEvent


class QuizQuestionDetail(BaseModel):
    question_id: str = Field(..., description="Unique ID for the question.")
    correct: bool = Field(..., description="Whether the answer was correct.")
    time_spent: float = Field(..., ge=0, description="Time spent on the question in seconds.")
    answer_text: Optional[str] = Field(None, description="User's answer if applicable.")
    feedback_text: Optional[str] = Field(None, description="Instructor's feedback if applicable.")


class QuizEvent(BaseEvent):
    event_type: Literal["quiz"] = "quiz"
    course_id: str = Field(..., description="Associated course ID.")
    quiz_id: str = Field(..., description="Unique identifier for the quiz.")
    attempt_id: str = Field(..., description="Unique identifier for this attempt.")
    quiz_type: str = Field(..., description="Type of quiz (e.g., multiple_choice, open-ended).")
    quiz_mode: str = Field(..., description="Mode of quiz (e.g., practice, exam).")
    score: float = Field(..., ge=0, description="Score achieved by the user.")
    max_score: float = Field(..., ge=0, description="Maximum possible score.")
    time_taken: float = Field(..., ge=0, description="Time taken to complete the quiz.")
    attempts_left: Optional[int] = Field(None, description="Remaining attempts.")
    questions: List[QuizQuestionDetail] = Field(..., description="Details of each question attempted during the quiz.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user999",
                "timestamp": "2025-01-31T12:00:00Z",
                "course_id": "course_789",
                "quiz_id": "quiz_123",
                "attempt_id": "attempt_456",
                "quiz_type": "multiple_choice",
                "quiz_mode": "exam",
                "score": 8.5,
                "max_score": 10,
                "time_taken": 600,
                "attempts_left": 2,
                "questions": [
                    {
                        "question_id": "q1",
                        "correct": True,
                        "time_spent": 30,
                        "answer_text": "A",
                        "feedback_text": "Good job!"
                    },
                    {
                        "question_id": "q2",
                        "correct": False,
                        "time_spent": 45,
                        "answer_text": "C",
                        "feedback_text": "Try reviewing this concept."
                    },
                ],
            }
        }
    }
