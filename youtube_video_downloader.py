import yt_dlp

def download_youtube_video():
    url = input("Enter the YouTube URL: ").strip()

    ydl_opts_info = {
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            # Only real video formats
            resolutions = sorted(
                {f['height'] for f in formats
                 if f.get('height') and f.get('vcodec') != 'none'},
                reverse=True
            )

            if not resolutions:
                print("No video resolutions found.")
                return

            print(f"\nTitle: {info.get('title')}")
            print("-" * 30)
            print("Available Qualities:")
            for i, res in enumerate(resolutions, 1):
                print(f"[{i}] {res}p")

            while True:
                try:
                    choice = int(input("\nSelect the number for quality: "))
                    if 1 <= choice <= len(resolutions):
                        break
                    print("Invalid choice. Try again.")
                except ValueError:
                    print("Enter a valid number.")

            selected_res = resolutions[choice - 1]

            ydl_opts_final = {
                'format': f'bestvideo[height<={selected_res}][vcodec!=none]+bestaudio/best',
                'outtmpl': '%(title)s_%(resolution)s.%(ext)s',
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'progress_hooks': [progress_hook],
            }

            print(f"\nDownloading {selected_res}p...")
            with yt_dlp.YoutubeDL(ydl_opts_final) as ydl_final:
                ydl_final.download([url])

            print("\n✅ Download Complete!")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownloading: {d['_percent_str']} at {d['_speed_str']}", end="")
    elif d['status'] == 'finished':
        print("\nMerging audio & video...")

if __name__ == "__main__":
    download_youtube_video()
