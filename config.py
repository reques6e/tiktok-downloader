from dotenv import dotenv_values


_config = dotenv_values('.env')

TIME_OUT: int = _config['TIME_OUT']
CHANNEL_ID: str = _config['CHANNEL_ID']
CHANNEL_LINK: str = _config['CHANNEL_LINK']