import PySimpleGUI as Sg

from pytube import YouTube, Search


class Video:
    def __init__(self, query: str):
        self.url: str = str()
        self.title: str = str()
        self.query: str = query

    def search(self) -> list[YouTube]:
        video_list = Search(self.query).results
        return video_list

    def download(self, vid: YouTube, a_only: bool = False):
        self.url = vid.watch_url
        self.title = vid.title
        if a_only:
            vid.streams.filter(only_audio=True).desc().first().download()
        else:
            vid.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution().download()


if __name__ == '__main__':
    Sg.theme('DarkTeal9')
    layout = [
        [Sg.Text("Search phrase:")],
        [Sg.InputText(key="-INPUT-")],
        [Sg.Radio("Video", 0), Sg.Radio("Audio", 0)],
        [Sg.Button(button_text="Search", key='-Q_BUTTON-')]
    ]
    window = Sg.Window("Search page", layout)
    while True:
        event, values = window.read()
        if event == Sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == "-Q_BUTTON-":
            if values[0]:
                audio_only = False
            else:
                audio_only = True
            window.close()
            q = values["-INPUT-"]
            video = Video(q)
            videos = video.search()
            layout1 = [[Sg.Button(button_text=f"{i + 1}", key=f"-B_{i + 1}"),
                        Sg.Text(f"Title: {token.title}")] for i, token in enumerate(videos)]
            layout1.append([Sg.Button(button_text="Exit", key="-QUIT-")])
            window1 = Sg.Window("Video list", layout1)
            while True:
                event, values = window1.read()
                if event == Sg.WINDOW_CLOSED or event == "-QUIT-":
                    window1.close()
                    break
                elif event.startswith("-B_"):
                    number = int(event.split("_")[1])-1
                    video.download(videos[number], audio_only)
