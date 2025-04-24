

class TikTokVideoDownloadError(Exception):
    """
    Ошибка при скачивании с TikTok. Возможно, ссылка устарела.
    """
    pass

class InstagramVideoDownloadError(Exception):
    """
    Поддерживаются только Reels и видео.
    """
    pass

class FileIsNotVideo(Exception):
    """
    Файл не является видео
    """
    pass

class UnknownDownloadError(Exception):
    """
    Неизвестная ошибка при скачивании видео.
    """
    pass