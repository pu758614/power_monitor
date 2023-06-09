from django.shortcuts import render
import vlc
# Create your views here.


def stream_view(request):
    rtsp_url = "rtsp://monitor:1qazxsw2@192.168.2.9:554/main_7"
    vlc_instance = vlc.Instance()
    media_player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(rtsp_url)
    media_player.set_media(media)
    media_player.play()

    context = {
        'media_player': media_player,
    }
    return render(request, 'stream.html', context)