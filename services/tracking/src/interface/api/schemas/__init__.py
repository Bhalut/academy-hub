from typing import Union

from .assignment import AssignmentEvent
from .base import BaseEvent
from .click import ClickEvent
from .feedback import FeedbackEvent
from .file_upload import FileUploadEvent
from .forum import ForumEvent
from .lesson import LessonEvent
from .login import LoginEvent
from .logout import LogoutEvent
from .progress import ProgressEvent
from .quiz import QuizEvent, QuizQuestionDetail

EventSchema = Union[
    ClickEvent,
    ProgressEvent,
    LoginEvent,
    QuizEvent,
    QuizQuestionDetail,
    ForumEvent,
    AssignmentEvent,
    FeedbackEvent,
    FileUploadEvent,
    LessonEvent,
    LogoutEvent,
]
