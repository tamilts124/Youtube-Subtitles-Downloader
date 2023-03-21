import requests, sys
from bs4 import BeautifulSoup
from urllib.parse import unquote

formats =['SRT', 'VTT', 'TXT']

def getSubtitles(pageurl):
    json =subripper.post('https://subripper.com/getinfo', data={'url': pageurl, 'token': token}).json()
    subtitles =[]
    if not json['status']=='success':
        return subtitles
    continer =BeautifulSoup(json['message'], 'html.parser').findAll('div', {'style': 'margin-bottom:15px'})[2:]
    for subcontiner in continer:
        subtitle =[]
        subtitle.append(str(subcontiner).split('</div>')[-2].replace('\n', ''))
        for a in subcontiner.findAll('a'):
            subtitle.append('https://subripper.com'+a['href'])
        subtitles.append(subtitle)
    return subtitles

def help():
    print('''
    Usage: Program.py youtubeurl format savepath
    
    youtubeurl - url of the youtube video page['require']
    format     - subtitle format['require]
    savepath   - where to save the subtitle['not mandatory']

    Conditions:

        youtubeurl - Must starts with 'https://www.youtube.com/'
        format     - 'SRT', 'VTT', 'TXT'
        savepath   - Must path ends with '/'
        ''')

def main():
    youtubeurl =sys.argv[1].strip(' \n\t')
    format =sys.argv[2].strip(' \n\t').upper()
    savepath =''
    if len(sys.argv)==4:
        savepath =sys.argv[3].strip(' \n\t')
    if not (youtubeurl.startswith('https://www.youtube.com/') and format in formats and (not savepath or savepath[-1]=='/')):
        help(); exit(1)
    subtitles =getSubtitles(youtubeurl)
    if not subtitles: print('\n> No Subtitle..'); return
    print('\n> Subtitles:\n')
    for n, subtitle in enumerate(subtitles, start=1):
        print('\t'+str(n)+'.', subtitle[0])
    print('\n\t'+str(len(subtitles)+1)+'.', 'Break')
    
    while True:
        try: opt =int(input('\n> Choice: '))
        except Exception: continue
        if not 0<opt<=len(subtitles)+1: continue
        if opt==len(subtitles)+1: break
        subtitle =subtitles[opt-1]
        if len(subtitle[1:])==len(formats):
            result =subripper.get(subtitle[1:][formats.index(format)])
            try:
                if not savepath:
                    savepath ='./'
                filename =unquote(result.headers['Content-Disposition'].split('"')[1])
                with open(savepath+filename, 'wt') as file:
                    file.write(result.text)
                print('\n>', filename)
            except PermissionError: print('\n> Not have a Permission to Write..')
        else: print('\n> Formats Need to Update..\n')

if __name__ == '__main__':
    if not len(sys.argv) in (3, 4):
        help(); exit(1)
    subripper =requests.session()
    subripper.headers ={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate'
    }
    token =subripper.get('https://subripper.com').text.split('name="token" value="')[1].split('"')[0]
    main()