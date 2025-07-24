import os
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, create_engine, ForeignKey, Integer, Table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, UTC

from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# -------------------- Users -------------------------------------------------------------------------
class User(Base):
    __tablename__ = 'rubikjanbot_users'

    telegram_id = Column(BigInteger, primary_key=True)  # ID пользователя в Telegram
    username = Column(String(50), nullable=True)  # @username (может быть None, если скрыт)
    first_name = Column(String(50), nullable=False)  # Имя
    last_name = Column(String(50), nullable=True)  # Фамилия (может быть None)
    phone = Column(String(20), nullable=True)  # Телефон (если пользователь его предоставит)
    is_admin = Column(Boolean, default=False)  # Админ ли?
    is_active = Column(Boolean, default=True)  # Активен ли аккаунт?
    registered_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))  # Дата регистрации

    def __repr__(self):
        return f"<User(id={self.telegram_id}, username='{self.username}')>"

# ------------------------------
# Категория товаров (например, Роллы, Пицца)
# ------------------------------
class Category(Base):
    __tablename__ = 'categories'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # Название категории
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


# ------------------------------
# Ингредиенты для продуктов (например, лосось, сыр)
# ------------------------------

# Таблица связи многие-ко-многим: какой товар содержит какие ингредиенты
product_ingredient_table = Table(
    'product_ingredients',
    Base.metadata,
    Column('product_id', BigInteger, ForeignKey('products.id'), primary_key=True),
    Column('ingredient_id', BigInteger, ForeignKey('ingredients.id'), primary_key=True)
)


# Справочник ингредиентов
class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)  # Например: "Лосось", "Сыр"

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"


# ------------------------------
# Товар (продукт в меню)
# ------------------------------
class Product(Base):
    __tablename__ = 'products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)         # Название товара
    description = Column(String(500), nullable=True)   # Описание товара
    price = Column(BigInteger, nullable=False)         # Цена в копейках
    image_url = Column(String(255), nullable=True)     # URL изображения
    category_id = Column(BigInteger, ForeignKey('categories.id'), nullable=False)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", backref="products")

    # Связь с ингредиентами
    ingredients = relationship(
        "Ingredient",
        secondary=product_ingredient_table,
        backref="products"
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


# ------------------------------
# Позиции в корзине пользователя
# ------------------------------
class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('rubikjanbot_users.telegram_id'), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False)
    quantity = Column(BigInteger, default=1)

    user = relationship("User", backref="cart_items")
    product = relationship("Product")

    def __repr__(self):
        return f"<CartItem(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"


# ------------------------------
# Заказ пользователя
# ------------------------------
class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('rubikjanbot_users.telegram_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
    status = Column(String(20), default='pending')  # pending, paid, delivering, delivered, canceled
    total_price = Column(BigInteger, nullable=False)  # Общая сумма заказа (в копейках)
    delivery_address = Column(String(255), nullable=False)  # Адрес доставки
    comment = Column(String(500), nullable=True)  # Комментарий к заказу

    user = relationship("User", backref="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, status='{self.status}')>"


# ------------------------------
# Конкретные товары в заказе
# ------------------------------
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False)
    quantity = Column(BigInteger, nullable=False)
    unit_price = Column(BigInteger, nullable=False)  # Цена на момент покупки

    order = relationship("Order", backref="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"


# ------------------------------
# Платёж по заказу
# ------------------------------
class Payment(Base):
    __tablename__ = 'payments'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('rubikjanbot_users.telegram_id'), nullable=False)
    amount = Column(BigInteger, nullable=False)  # Сумма (в копейках)
    payment_time = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))
    status = Column(String(20), default='pending')  # pending, success, failed
    payment_method = Column(String(50), nullable=True)  # Например, card, cash

    order = relationship("Order", backref="payment")
    user = relationship("User")

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, amount={self.amount}, status='{self.status}')>"


# ------------------------------
# Информация о доставке заказа
# ------------------------------
class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    courier_name = Column(String(100), nullable=True)
    courier_phone = Column(String(20), nullable=True)
    status = Column(String(20), default='preparing')  # preparing, on_the_way, delivered
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    order = relationship("Order", backref="delivery")

    def __repr__(self):
        return f"<Delivery(id={self.id}, order_id={self.order_id}, status='{self.status}')>"




# ------------------------------
# Подключение к базе
# ------------------------------
engine = create_engine(
    os.getenv("RUBIKJANBOT_DATABASE_URL", "sqlite:///rubikjanbot.db"),
    echo=True)

AsyncSessionLocal = None


if RUBIKJANBOT_ASYNC_DATABASE_URL := os.getenv("RUBIKJANBOT_ASYNC_DATABASE_URL"):
    async_engine = create_async_engine(
        os.getenv("RUBIKJANBOT_ASYNC_DATABASE_URL", "sqlite+aiosqlite:///rubikjanbot.db"),
        echo=True
    )
    AsyncSessionLocal = sessionmaker (async_engine, class_=AsyncSession, expire_on_commit=False) 
