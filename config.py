import os

PORT = 8000

MAX_IMAGE_SIZE = 20  # Max image size in MB
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png"]

NSFW_USERNAME = os.getenv("NSFW_USERNAME", "")
NSFW_PASSWORD = os.getenv("NSFW_PASSWORD", "")
