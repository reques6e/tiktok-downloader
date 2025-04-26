from bs4 import BeautifulSoup, FeatureNotFound


def validate_html_structure(text: str) -> bool:
    """Проверяет, что текст содержит валидные HTML-теги для Telegram"""
    try:
        allowed_tags = {'b', 'strong', 'i', 'em', 'u', 'ins', 's', 'strike', 'del', 'a', 'code', 'pre'}
        
        soup = BeautifulSoup(text, 'html.parser')
        
        for tag in soup.find_all(True):  
            if tag.name not in allowed_tags:
                return False  
            
            if tag.name == 'a' and not tag.get('href'):
                return False
        
        return True
    
    except Exception:
        return False