from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from slp_admin.models import *


def quiz(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)

        quiz = Quiz.objects.all()
        context = {"quiz": quiz,'name':admin_info.first_name}
        return render(request, "quiz.html", context)


def edit_quiz(request, quiz_id):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
    
        quiz = Quiz.objects.get(id=quiz_id)
        context = {"quiz": quiz,'name':admin_info.first_name, "count": len(quiz.question)}
        return render(request, "edit-questions.html", context)

    if request.method == 'POST':
        count = request.POST['count']

        questions = Question.objects.filter(quiz=quiz_id)
        for question in questions:
            question.delete()

        quiz = Quiz.objects.filter(id=quiz_id).update(
            question=[]
        )
        quiz_new = Quiz.objects.get(id=quiz_id)

        if int(count) > 1:
            for i in range(1, int(count) + 1):
                j = str(i)
                question = request.POST['q' + j]
                option1 = request.POST['q' + j + '_1']
                option2 = request.POST['q' + j + '_2']
                option3 = request.POST['q' + j + '_3']
                option4 = request.POST['q' + j + '_4']
                correct_answer = request.POST['q' + j + '_correct']
                ques_obj = Question.objects.create(
                    quiz=quiz_id,
                    question=question,
                    option_1=option1,
                    option_2=option2,
                    option_3=option3,
                    option_4=option4,
                    correct_answer=correct_answer
                )
                ques_obj.save()
                quiz_new.question.append(ques_obj)
                quiz_new.save()
            return redirect('quiz')
        else:
            question = request.POST['q1']
            option1 = request.POST['q1_1']
            option2 = request.POST['q1_2']
            option3 = request.POST['q1_3']
            option4 = request.POST['q1_4']
            correct_answer = request.POST['q1_correct']
            ques_obj = Question.objects.create(
                quiz=quiz_id,
                question=question,
                option_1=option1,
                option_2=option2,
                option_3=option3,
                option_4=option4,
                correct_answer=correct_answer
            )
            ques_obj.save()
            quiz_new.question.append(ques_obj)
            quiz_new.save()
        return redirect('quiz')


def delete_quiz(request, quiz_id):
    if request.method == 'GET':
        quiz_info = Quiz.objects.get(id=quiz_id)
        quiz_info.is_deleted = True

        ques = Question.objects.filter(quiz=quiz_id)
        for info in ques:
            info.is_deleted = True
            info.save()
        quiz_info.save()
        return redirect('quiz')


def view_quiz(request, quiz_id):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
    
        quiz = Quiz.objects.get(id=quiz_id)
        context = {"quiz": quiz,'name':admin_info.first_name}
        return render(request, "view-questions.html", context)



@api_view(['GET', 'POST'])
def add_question(request):
    if request.method == 'POST':
        quiz_name = request.POST['quiz_name']
        points = request.POST['points']
        point = int(points)
        video_name = request.POST['video_select']
        video = Video.objects.get(title=video_name)
        count = request.POST['count']

        quiz = Quiz.objects.create(
            name=quiz_name,
            video=video,
            points=point,
            question=[]
        )
        if int(count) > 1:
            for i in range(1, int(count) + 1):
                j = str(i)
                question = request.POST['q' + j]
                option1 = request.POST['q' + j + '_1']
                option2 = request.POST['q' + j + '_2']
                option3 = request.POST['q' + j + '_3']
                option4 = request.POST['q' + j + '_4']
                correct_answer = request.POST['q' + j + '_correct']
                ques_obj = Question.objects.create(
                    quiz=quiz.id,
                    question=question,
                    option_1=option1,
                    option_2=option2,
                    option_3=option3,
                    option_4=option4,
                    correct_answer=correct_answer
                )
                ques_obj.save()
                quiz.question.append(ques_obj)
                quiz.save()
            return redirect('quiz')
        else:
            question = request.POST['q1']
            option1 = request.POST['q1_1']
            option2 = request.POST['q1_2']
            option3 = request.POST['q1_3']
            option4 = request.POST['q1_4']
            correct_answer = request.POST['q1_correct']
            ques_obj = Question.objects.create(
                quiz=quiz.id,
                question=question,
                option_1=option1,
                option_2=option2,
                option_3=option3,
                option_4=option4,
                correct_answer=correct_answer
            )
            ques_obj.save()
            quiz.question.append(ques_obj)
            quiz.save()
            return redirect('quiz')

    if request.method == 'GET':
        try:
            admin_session = request.session['Admintoken']
        except:
            redirect("slpdashboard")

        if request.method == 'GET':
            admin_token = AdminToken.objects.get(token=admin_session)
            admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
            video_info = Video.objects.filter(quiz__isnull=True)
            quiz_info = Quiz.objects.filter(is_deleted=True)
            print(quiz_info)
            context = {"videos": video_info, "quiz": quiz_info,'name':admin_info.first_name}
            return render(request, "add-questions.html", context)
