from table_class import Table
from tg_bot.config import load_config

config = load_config(".env")


workTable = Table(config.misc.credentials_file)