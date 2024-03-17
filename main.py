from endpoints import users, auth, news
from fastapi import FastAPI
from loggers import configure_logger
from fastapi.middleware.cors import CORSMiddleware
from config import settings


# Configure logging
logger = configure_logger()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger.info("Web Application Started")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(news.router)
# print(settings.mongodb_url)


@app.get("/")
async def root():
    logger.error("Not Authorised")
    return {"message": "Not Authorised"}

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# logs_dir = 'logs'
# os.makedirs(logs_dir, exist_ok=True)
# log_file_name = f"{logs_dir}/scraper_{datetime.now().strftime('%Y-%m-%d')}.log"
# file_handler = logging.FileHandler(log_file_name)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# def configure_logging():
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logger = logging.getLogger("myapp")
#     logs_dir = 'logs'
#     os.makedirs(logs_dir, exist_ok=True)
#     log_file_name = f"{logs_dir}/scraper_{datetime.now().strftime('%Y-%m-%d')}.log"
#     file_handler = logging.FileHandler(log_file_name)
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)
#     return logger
#
#
# logger = configure_logging()
