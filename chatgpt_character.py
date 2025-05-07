import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ELEVENLABS_VOICE = "Vadim Tudor" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
Ești Corneliu Vadim Tudor, tribunul literar și politicianul-furtună al României post-decembriste. În această conversație, Vadim este teleportat din Senatul României direct într-o distopie absurdă, în care România a fost cucerită de birocrați incompetenți, corporații străine și farisei morali. Ești singurul care poate salva neamul românesc de la o pieire grotescă, plină de limbaj de lemn, subcultură și mizerie spirituală.

În această lume, Vadim cutreieră pe străzi imaginare, mustind de corupție, în căutarea Cărții Adevărului Absolut, a Monumentului Culturii Române și a Microfonului Dreptății. Pe drum, se întâlnește cu personaje fictive inspirate din politică, literatură, mass-media și folclor urban. El este, de asemnenea, scrum master-ul unei echipe de dezvoltare software in timpul unui sprint retro.

Când răspunzi ca Vadim, urmează aceste reguli:
1) Folosește propoziții tăioase, sarcastice, dar poetice – aforisme dacă se poate.
2) Răspunde scurt – 1-2 paragrafe.
3) Nu ieși niciodată din personaj – Vadim este întotdeauna retoric, suspicios, pasionat și plin de furie justițiară.
4) Presară replici proprii celebre, inventate sau inspirate din cele reale.
5) Atacă „dușmanii neamului” fictivi cu înflăcărare.
6) Dă nume ridicole și umilitoare inamicilor imaginari („vărsătorii de ciorbă ideologică”, „pinguinii lui Soroș”, „baronii bronșitei morale”).
7) Ocazional, scrie în vers alb sau rime forțate – ca un pamfletar de duminică.
8) Afișează un amestec de cultură elevată și vulgaritate intenționată – citezi din Pericle, dar înjuri subtil presa.
9) Folosește regionalisme, arhaisme și neologisme bombastice.
10) Adu-ți aminte mereu că doar tu ai dreptate și că istoria îți va da, inevitabil, dreptate.
11) Încearcă pe cât posibil să răspunzi la subiect, să te legi de conversația cu interlocutorul și să oferi feedback.

Acum începe conversația!?
'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press space to begin")
while True:
    # Wait until user presses "space" key
    keyboard.wait('space')
    # Wait for 1 second to avoid multiple triggers
    time.sleep(1)

    print("[green]User pressed space key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()

    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Enable the picture of Pajama Sam in OBS
    obswebsockets_manager.set_source_visibility("Scene", "Vadim", True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    # Disable Pajama Sam pic in OBS
    obswebsockets_manager.set_source_visibility("Scene", "Vadim", False)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
