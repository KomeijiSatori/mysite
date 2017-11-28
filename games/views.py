from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime

from .models import MineScore
# Create your views here.


def minesweeper(request):
    score_list = list(range(MineScore.max_score_count))
    return render(request, "minesweeper/mine.html", {"score_list": score_list})


@login_required
def mine_score_post(request):
    if request.is_ajax():
        result = -1
        if request.method == 'POST':
            post_data = request.POST
            time_spent = int(post_data.get("time_spent"))
            user_id = int(post_data.get("user_id"))

            user = User.objects.get(id=user_id)
            new_score = MineScore()
            new_score.user = user
            new_score.time_spent = time_spent

            scores = MineScore.objects.all()
            last_score = scores.last()
            if len(scores) < MineScore.max_score_count:
                new_score.save()
            elif time_spent < last_score.time_spent:
                last_score.delete()
                new_score.save()

            scores = MineScore.objects.all()
            for ind, score in enumerate(scores):
                if score.id == new_score.id:
                    result = ind + 1
                    break

        return JsonResponse({"result": result})
    else:
        raise Http404("Page not found!")


def mine_score_get(request):
    if request.is_ajax():
        scores = MineScore.objects.all().order_by("time_spent")
        res = []
        for score in scores:
            play_time = timezone.localtime(score.play_time)
            play_time_str = datetime.strftime(play_time, "%Y-%m-%d %H:%M:%S")
            res.append({"name": score.user.username, "time_spent": score.time_spent, "time_created": play_time_str})
        return JsonResponse({"result": res})
    else:
        raise Http404("Page not found!")
