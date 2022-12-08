"""
test.py file contains classes that
support testcommands.py file.
Some classes define question storage
and others define answers from students storage.
"""

import datetime

class Test :
    def __init__(self,name):
        self.name_of_test = name
        self.date = str(datetime.datetime.now())
        #type 0 are questions where students are called to write on a topic.
        #type 1 are questions where students need to pick only one answer.
        #type 2 are questions where students can pick multiple answers .
        self.question_type_0 = []
        self.question_type_1 = []
        self.question_type_2 = []
        self.question_objects = []
        self.types_by_position = []
    def get_types_by_position(self):
        return self.types_by_position
    def get_question_objects(self):
        return self.question_objects
    def get_name_of_test(self):
        return self.name_of_test
    def add_question_objects(self,question_objects_list):
        self.question_objects = question_objects_list

    def add_question_0(self,question):
        self.question_type_0.append(question)
        self.types_by_position.append("0")
    def add_question_1(self,question):
        self.question_type_1.append(question)
        self.types_by_position.append("1")
    def add_question_2(self,question):
        self.question_type_2.append(question)
        self.types_by_position.append("2")
class Questions:
    def __init__(self,belongs_to_test,position,type_of_question,main_body):
        self.position = position
        self.belongs_to_test = belongs_to_test
        self.type_of_question = type_of_question
        self.main_body = main_body
    def get_position(self):
        return self.position
    def get_test(self):
        return self.belongs_to_test
    def get_type(self):
        return self.type_of_question
    def get_main_body(self):
        return self.main_body
    def set_position(self,position):
        self.position = position
    def set_test(self,test):
        self.belongs_to_test = test
    def set_type(self,type_of_question):
        self.type_of_question = type_of_question
    def set_main_body(self,main_body):
        self.main_body = main_body
class Question_type_0(Questions) :
    def __init__(self,belongs_to_test,position,type_of_question,main_body):
        super().__init__(belongs_to_test,position,type_of_question,main_body)
class Question_type_1(Questions):
    def __init__(self,belongs_to_test,position,type_of_question,main_body,probable_answers,correct_answer):
        super().__init__(belongs_to_test,position,type_of_question,main_body)
        self.probable_answers = probable_answers
        self.correct_answer = int(correct_answer)
        self.number_of_correct_answers = 1
    def get_probable_answers(self):
        return self.probable_answers
    def get_correct_answers(self):
        return self.correct_answer
    def get_number_of_correct_answers(self):
        return self.number_of_correct_answers
class Question_type_2(Questions):
    def __init__(self,belongs_to_test,position,type_of_question,main_body,probalbe_answers,correct_answers):
        super().__init__(belongs_to_test,position,type_of_question,main_body)
        self.probable_answers = probalbe_answers
        self.correct_answers = []
        correct_answer_strings = correct_answers.split(",")
        for i in correct_answer_strings:
            self.correct_answers.append(int(i))
        self.number_of_correct_answers = len(self.correct_answers)
    def get_correct_answers(self):
        return self.correct_answers
    def get_number_of_correct_answers(self):
        return self.number_of_correct_answers
    def get_probable_answers(self):
        return self.probable_answers

"""
this class wasn't needed but it will remain here in case of future use.


class Test_answers_set:
    def __init__(self,name_of_test_set):
        self.name_of_test_set = name_of_test_set
        self.date = str(datetime.datetime.now())
        self.test_answers = [] #test #1 answers of students , test #2 answers of students etc.
    def add_test_answers(self,test_answers_object):
        self.test_answers.append(test_answers_object)
"""

class Test_answers :
    def __init__(self,name_of_test):
        self.name_of_test = name_of_test
        self.date = str(datetime.datetime.now())
        self.student_answers = [] #student #0 answers, student #1 answers etc.
    def get_student_answers(self):
        return self.student_answers
    def get_name_of_test(self):
        return self.name_of_test
    def add_student_answers(self,student_answers_object):
        self.student_answers.append(student_answers_object)
class Student_answers :
    def __init__(self,name_of_student):
        self.name_of_student = name_of_student
        self.date = str(datetime.datetime.now())
        # type 0 are answers which are text.
        # type 1 are answers with only one element.
        # type 2 are answers with multiple elements .
        self.answer_type_0 = []
        self.answer_type_1 = []
        self.answer_type_2 = []
        self.answer_objects = []
        self.answer_types_by_position = []
    def get_types_by_position(self):
        return self.answer_types_by_position
    def get_type_by_position(self,i):
        return self.answer_types_by_position[i]
    def get_answer_objects(self):
        return self.answer_objects
    def get_answer_object(self,i):
        return self.answer_objects[i]
    def get_student_name(self):
        return self.name_of_student
    def add_answer_objects(self,answer_objects_list):
        self.answer_objects = answer_objects_list
    def add_answer_0(self,answer):
        self.answer_type_0.append(answer)
        self.answer_types_by_position.append("0")
    def add_answer_1(self,answer):
        self.answer_type_1.append(answer)
        self.answer_types_by_position.append("1")
    def add_answer_2(self,answer):
        self.answer_type_2.append(answer)
        self.answer_types_by_position.append("2")
class Answers :
    def __init__(self,belongs_to_test,belongs_to_student,position,type_of_answer,answer_body):
        self.position = position
        self.belongs_to_test = belongs_to_test
        self.type_of_answer = type_of_answer
        self.belongs_to_student = belongs_to_student
        self.answer_body = answer_body
    def get_answer_body(self):
        return self.answer_body
    def get_position(self):
        return self.position
    def get_test(self):
        return self.belongs_to_test
    def get_type(self):
        return self.type_of_answer
    def get_student(self):
        return self.belongs_to_student
class Answer_type_0(Answers):

    def __init__(self,belongs_to_test,belongs_to_student,position,type_of_answer,answer_body):
        super().__init__(belongs_to_test,belongs_to_student,position,type_of_answer,answer_body)
class Answer_type_1(Answers):
    def __init__(self,belongs_to_test,belongs_to_student,position,type_of_answer,answer_body):
        super().__init__(belongs_to_test,belongs_to_student,position,type_of_answer,answer_body)
        self.answer_body = int(answer_body)
    def get_answer_body(self):
        return self.answer_body
class Answer_type_2(Answers):
    def __init__(self,belongs_to_test,belongs_to_student,position,type_of_answer,answer_body):
        super().__init__(belongs_to_test,belongs_to_student,position,type_of_answer,answer_body)
        self.answer_body = []
        answer_body_strings = answer_body.split(",")
        for i in answer_body_strings:
            self.answer_body.append(int(i))
    def get_answer_body(self):
        return self.answer_body

