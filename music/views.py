from django.shortcuts import render, redirect, get_object_or_404
from .models.song import Song
from .models.status import Status
from .services.strategy import get_song_generator


def create_song(request):
    if request.method == "POST":
        title = request.POST.get('title', 'Untitled')
        genre = request.POST.get('genre', '')
        lyrics = request.POST.get('lyrics', '')

        generator = get_song_generator()
        
        result = generator.generate({
            "title": title,
            "genre": genre,
            "lyrics": lyrics
        })

        new_song = Song.objects.create(
            user=request.user,
            title=title,
            genre=genre,
            lyrics=lyrics,
            status="Pending",
            task_id=result.get('task_id')
        )

        return redirect('song_detail', song_id=new_song.id)

    return render(request, 'music/create_form.html')


def check_music_progress(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if song.status == "Pending" and song.task_id:
        generator = get_song_generator()
        result = generator.check_status(song.task_id)

        if result.get('status') == "SUCCESS":
            song.status = "Completed"
            song.song_url = result.get('song_url')
            song.save()

    return render(request, 'music/song_detail.html', {'song': song})
