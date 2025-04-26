import time

from sqlalchemy import create_engine, Column, Integer, Boolean, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True)
    is_admin = Column(Boolean, default=False)
    # in_channel = Column(Boolean, default=False)

class Timeout(Base):
    __tablename__ = 'timeout'

    telegram_id = Column(BigInteger, primary_key=True)
    end_time = Column(Integer)

class Database:
    def __init__(self, db_url='sqlite:///data/database.db'):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_user(self, telegram_id):
        """Создание пользователя"""
        if not self.session.query(User).filter(User.telegram_id == telegram_id).first():
            new_user = User(telegram_id=telegram_id)
            self.session.add(new_user)
            self.session.commit()

    def set_admin(self, telegram_id):
        """Назначение пользователя админом"""
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.is_admin = True
            self.session.commit()

    # def set_channel_status(self, telegram_id: int, new_status: bool):
    #     """Обновление статуса канала"""
    #     user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
    #     if user:
    #         user.in_channel = new_status
    #         self.session.commit()

    def remove_admin(self, telegram_id):
        """Снятие пользователя с админки"""
        user = self.session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            user.is_admin = False
            self.session.commit()

    def add_timeout(self, telegram_id, duration_seconds):
        """Добавление пользователя в таймаут с указанием времени окончания"""
        end_time = int(time.time()) + duration_seconds
        timeout = Timeout(telegram_id=telegram_id, end_time=end_time)
        self.session.add(timeout)
        self.session.commit()

    def update_timeout(self, telegram_id, duration_seconds):
        """Обновление времени окончания таймаута для пользователя"""
        end_time = int(time.time()) + duration_seconds
        timeout = self.session.query(Timeout).filter(Timeout.telegram_id == telegram_id).first()
        if timeout:
            timeout.end_time = end_time
            self.session.commit()

    def check_timeout(self, telegram_id):
        """Проверка, есть ли у пользователя активный таймаут"""
        timeout = self.session.query(Timeout).filter(Timeout.telegram_id == telegram_id).first()
        if timeout.end_time > int(time.time()):
            return True  # Таймаут активен
        return False  # Таймаут не активен или уже завершен

    def get_user(self, telegram_id):
        """Получение пользователя по telegram_id"""
        return self.session.query(User).filter(User.telegram_id == telegram_id).first()

    def get_users(self):
        """Получение списка всех пользователей"""
        return self.session.query(User).all()

    def user_exists(self, telegram_id):
        """Проверка существования пользователя"""
        return self.session.query(User).filter(User.telegram_id == telegram_id).first() is not None

    def close(self):
        """Закрытие сессии"""
        self.session.close()
