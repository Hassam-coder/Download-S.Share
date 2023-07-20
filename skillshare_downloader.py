import subprocess
import os
import shutil
import re

# Install required modules
subprocess.check_call(["pip", "install", "requests", "tqdm", "click", "termcolor", "pyfiglet","youtube-dl"])

# Import required modules
import requests
import subprocess
from tqdm import tqdm
import click
from termcolor import colored
import pyfiglet


def display_title(title):
    ascii_art = pyfiglet.figlet_format(title, font='slant')
    colored_ascii_art = colored(ascii_art, 'green')
    click.echo_via_pager(colored_ascii_art)

    click.echo('\n')
    copyright_text = colored('© Hassam Moin.', 'cyan')
    click.echo(click.style(copyright_text.center(shutil.get_terminal_size().columns), dim=True))


# Clear screen and display title
os.system('cls' if os.name == 'nt' else 'clear')
display_title('SKILLSHARE DOWNLOADER')


@click.command()
def main():
    class_link = click.prompt('\nEnter the Skillshare class link')
    class_id = class_link.strip().split('/')[-1]

    api_url = f'https://skillapi.knavv.repl.co/class/{class_id}'

    response = requests.get(api_url)

    if response.status_code != 200:
        click.echo('Failed to fetch course information')
        exit()

    data = response.json()

    if 'course_name' not in data or 'videos' not in data:
        click.echo('Invalid course information')
        exit()

    course_name = data['course_name']
    videos = data['videos']

    click.echo(f'\nCourse Name: {course_name}\n')

    # Remove invalid characters from output directory name
    output_dir = re.sub(r'[<>:"/\\|?*]', '_', course_name).replace(' ', '_')

    click.echo(f'Creating directory: {output_dir}\n')
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=len(videos), unit='videos', desc='Downloading videos') as pbar:
        for video in videos:
            video_name = video['name']
            video_url = video['url']

            output_file = f'{output_dir}/{video_name}.mp4'

            subprocess.run(['youtube-dl', '-q', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', '-o', output_file, video_url], shell=True)
            pbar.update(1)

    click.echo('\n')
    click.echo(colored('All videos downloaded!', 'green', attrs=['bold']))


if __name__ == '__main__':
    main()
