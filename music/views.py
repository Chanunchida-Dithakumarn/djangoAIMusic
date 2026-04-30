from django.shortcuts import render, redirect, get_object_or_404
from .models.song import Song
from .models.status import Status
from .services.strategy import get_song_generator
from django.contrib.auth.decorators import login_required


@login_required
def generate_song(request):
    if request.method == "POST":
        title = request.POST.get('title', 'Untitled')
        genre = request.POST.get('genre', '')
        mood = request.POST.get('mood', '')
        visibility = request.POST.get('visibility', 'private')
        additional = request.POST.get('additional', '')

        generator = get_song_generator()
        
        result = generator.generate({
            "title": title,
            "genre": genre,
            "mood": mood,
            "visibility": visibility,
            "additional": additional
        })

        new_song = Song.objects.create(
            user=request.user,
            title=title,
            genre=genre,
            mood=mood,
            visibility=visibility,
            additional=additional,
            # status="Pending",
            task_id=result.get('task_id')
        )

        return redirect('song_detail', song_id=new_song.id)

    return render(request, 'music/song_config.html')


def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if song.status == "Pending" and song.task_id:
        generator = get_song_generator()
        result = generator.check_status(song.task_id)

        if result.get('status') == "Completed":
            song.status = "Completed"
            song.song_url = result.get('song_url')
            song.save()

    return render(request, 'music/song_detail.html', {'song': song})

