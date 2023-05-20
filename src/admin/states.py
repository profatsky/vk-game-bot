from vkbottle import BaseStateGroup


class UnansweredQuestionsState(BaseStateGroup):
    SHOW_UNANSWERED_QUESTIONS = 0
    ANSWER_QUESTION = 1


class AnsweredQuestionsState(BaseStateGroup):
    SHOW_ANSWERED_QUESTIONS = 0
    GET_INFO = 1
