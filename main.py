from pytube import YouTube, Search


class Video:
    def __init__(self, query: str):
        self.url: str = str()
        self.title: str = str()
        self.query: str = query

    def search(self) -> list[YouTube]:
        video_list = Search(self.query).results
        return video_list

    def download(self, vid: YouTube, audio_only: bool):
        self.url = vid.watch_url
        self.title = vid.title
        if audio_only:
            vid.streams.filter(only_audio=True).desc().first().download()
        else:
            vid.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution().download()


if __name__ == '__main__':
    q = input("Search: \n")
    video = Video(q)
    videos = video.search()
    for i, token in enumerate(videos):
        print(f"[{i + 1}] Title: {token.title}")

    try:
        numer = int(input("Your choice: ")) - 1
        wybor = videos[numer]
        video.download(wybor, True)
    except ValueError as e:
        print("USER HAS ENTERED NON-INTEGER! ERROR CODE: 101")
        exit(100)
