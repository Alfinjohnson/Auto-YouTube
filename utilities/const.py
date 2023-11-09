from datetime import datetime

NEWS_API_KEY: str = 'NEWS_API_KEY'
NEWS_FETCH_LIMIT: int = 10

AWS_ACCESS_KEY: str = 'AWS_ACCESS_KEY'
AWS_SEC_KEY: str = 'AWS_SEC_KEY'

EXISTING_TOPICS: str = '/YT/topic/existing_topics.json'

DRAFT_TOPIC: str = 'draft'
SAVED_TOPIC: str = 'saved'
S3_BUCKET: str = 'ytauto'

YT_SECRET_FILE: str = '/YT/cred/client_secret.json'
GCP_API_KEY: str = 'GCP_API_KEY'
CHANNEL_ID = 'YT_CHANNEL_ID'

YOUR_OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"
GPT_MODEL: str = 'text-davinci-003'


def get_current_date():
    return str(datetime.now().strftime('%d-%m-%Y-%M-%S'))


# create and map following directories
OUTPUT_AUDIO: str = '/YT/audio/'
OUTPUT_TRANSCRIPT: str = '/YT/transcript/'
STOCK_VIDEO_FOLDER: str = '/YT/video/'
OUTPUT_TMP: str = '/YT/tmp/'
OUTPUT_FINAL_VIDEO: str = '/YT/final/video/'
OUTPUT_FINAL_INFO: str = '/YT/final/info/'

LOG_PATH: str = '/YT/logs/main.log'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']

NEWS_TEST_RESPONSE = [{'title': "Sentinels announce partnership with OTK &amp; MoistCr1TiKal's Starforge",
                       'link': 'https://www.dexerto.com/business/sentinels-announce-partnership-with-otk-moistcr1tikals-starforge-2145269/',
                       'keywords': ['Business', 'Esports', 'Tech'], 'creator': ['Luís Mira'], 'video_url': None,
                       'description': 'Sentinels have announced a partnership with Starforge Systems, the PC building company founded by OTK and MoistCr1TiKaL.',
                       'content': 'The partnership sees the recently launched hardware company become the official PC supplier for ’ esports players and their content creator roster. They will receive the Voyager Creator Elite, Starforge Systems’ top-of-the-line PC, which has a retail price of $4,299.99 USD. The computer’s specs include an Intel Core i9-13900K CPU, Teamgroup Delta RGB 64GB DDR5 RAM and a GeForce RTX™ 4090 Graphics Card. “As a creator-led PC brand, Starforge places a high value on authentic and engaging content,” Starforge Systems CEO Nicholas Dankner told Dexerto. “We felt that Sentinels was highly aligned with Starforge in that regard, and we are excited for the opportunity to create substantive content together.” Subscribe to our newsletter for the latest updates on Esports, Gaming and more. It’s time. This is the first esports partnership of its kind from Starforge Systems, by OTK – the influencer organization that manages big names like Asmongold and Emiru – and MoistCr1TiKaL. , with prices starting at $1,149.99 USD. Self-described as “one of the fastest growing esports organizations in North America,” Sentinels field esports teams in Valorant, Apex Legends, and Halo. Their roster of creators is made up of Tarik ‘tarik’ Celik, Jared ‘zombs’ Gitlin, Brandon ‘aceu’ Winn, and Daphne ’39Daph’ Wai. Asked if further partnerships with more esports organizations are on the horizon, Dankner said: “At this time, our focus is on delivering an amazing partnership experience and amazing hardware to Sentinels. Our team commits fully to everything we do, and our partnership with Sentinels is no exception.”',
                       'pubDate': '2023-05-15 17:02:25', 'image_url': None, 'source_id': 'dexerto',
                       'category': ['technology'], 'country': ['united kingdom'], 'language': 'english'},
                      {'title': 'How to connect a PS4 controller to a PC',
                       'link': 'https://www.dexerto.com/tech/how-to-connect-a-ps4-controller-to-a-pc-2038712/',
                       'keywords': ['Gaming', 'PCs', 'Tech'], 'creator': ['Joel Loynds'], 'video_url': None,
                       'description': 'Getting your PS4 controller to connect to a PC is as simple as apple pie, with a few options for how you want to do it.',
                       'content': 'The is still one of the most popular among enthusiasts thanks to its form factor and integrated gyro; it’s a reliable peripheral that can pretty much do it all. As PC and gaming continues to blend, it’s no surprise to see games supporting the controller on both platforms. However, getting your PS4 controller to play nice with older titles or even games can be a bit of a hassle. On the other hand, platforms like and some games from the can translate the PS4’s inputs to your game without any extra software. This isn’t foolproof, so we’ll explore some tried-and-true methods so you can use your controller on PC. Pairing the PS4 controller over Bluetooth Ensure you have a Bluetooth dongle, or built-in Bluetooth before you do this. Go to your settings via Start > Settings > Bluetooth & devices. Also, ensure that you’re currently discoverable by Bluetooth. In the list of devices, keep an eye on the PS4 controller appearing under ‘PlayStation 4 controller’. Press the share and PS button until the backlight starts flashing. Your controller should now be in pairing mode. Go back to the Windows settings and connect the device together. Using a wired PlayStation 4 controller on a PC This is actually much simpler. If you’re playing via Steam, the software should pick it up for you automatically. You’ll need a micro USB cable to do this. If you’re not getting any response from your game after connecting it, you might need to convert the signal to XInput. The PS4 uses DirectInput, which some games don’t read. For this, we’ll need to use DS4Windows. Subscribe to our newsletter for the latest updates on Esports, Gaming and more. How to play Game Pass PC games with PlayStation 4 controller Using DS4Windows will let you play pretty much any game on your PC with your PS4 controller. It takes the DirectInput, and then converts it to the correct XInput. To download DS4Windows, just , and follow the installation instructions. After this, you can remap the controller to how you see fit, or even just use it as the default. X becomes A, Square is X, that sort of thing. It’ll also let you connect wirelessly over Bluetooth and track your battery. | | | | | | | |',
                       'pubDate': '2023-05-15 16:43:54', 'image_url': None, 'source_id': 'dexerto',
                       'category': ['technology'], 'country': ['united kingdom'], 'language': 'english'}
                      ]

BUSINESS_NEWS: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&country=ca,de,in,gb,us&language=en&category=business"
APPLE_NEWS: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=apple&language=en&category=technology,world"
TECH_NEWS: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&country=ca,de,in,gb,us&language=en&category=technology"
ELON_MUSK_NEWS: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=Elon%20Musk&language=en&category=technology,world"
