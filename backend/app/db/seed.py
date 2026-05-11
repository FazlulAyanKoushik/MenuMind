"""Seed script: creates 1 admin, 2 sample restaurants, 2 consumers, sample menus"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory, engine, Base
from app.core.security import hash_password
from app.core.constants import UserRole, RestaurantStatus, PlanTier
from app.modules.auth.model import User
from app.modules.tenants.model import Restaurant
from app.modules.menus.model import MenuItem
from app.modules.users.model import ConsumerProfile
from app.modules.admin import model as admin_model
from app.modules.knowledge_base import model as kb_model
from app.modules.qr import model as qr_model
from app.modules.chats import model as chat_model


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        admin = User(
            email="admin@menumind.com",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
        )
        db.add(admin)

        owner1 = User(
            email="owner@pizzeria.com",
            password_hash=hash_password("owner123"),
            role=UserRole.OWNER,
        )
        db.add(owner1)

        owner2 = User(
            email="owner@sushi.com",
            password_hash=hash_password("owner123"),
            role=UserRole.OWNER,
        )
        db.add(owner2)

        consumer1 = User(
            email="alice@example.com",
            password_hash=hash_password("consumer123"),
            role=UserRole.CONSUMER,
        )
        db.add(consumer1)

        consumer2 = User(
            email="bob@example.com",
            password_hash=hash_password("consumer123"),
            role=UserRole.CONSUMER,
        )
        db.add(consumer2)

        await db.flush()

        profile1 = ConsumerProfile(
            user_id=consumer1.id,
            preferences=["spicy", "vegetarian"],
            allergies=["peanuts"],
            region="South Asian",
        )
        db.add(profile1)

        profile2 = ConsumerProfile(
            user_id=consumer2.id,
            preferences=["seafood"],
            allergies=["gluten", "lactose"],
            region="Mediterranean",
        )
        db.add(profile2)

        restaurant1 = Restaurant(
            name="Tony's Pizzeria",
            slug="tonys-pizzeria",
            owner_id=owner1.id,
            status=RestaurantStatus.ACTIVE,
            plan=PlanTier.PRO,
        )
        db.add(restaurant1)

        restaurant2 = Restaurant(
            name="Sakura Sushi",
            slug="sakura-sushi",
            owner_id=owner2.id,
            status=RestaurantStatus.ACTIVE,
            plan=PlanTier.FREE,
        )
        db.add(restaurant2)

        await db.flush()

        pizza_items = [
            MenuItem(restaurant_id=restaurant1.id, name="Margherita", description="Classic tomato, mozzarella, basil", price=12.99, category="Pizza", ingredients=["tomato", "mozzarella", "basil", "olive oil"], allergens=["dairy"], cuisine_type="Italian", is_available=True),
            MenuItem(restaurant_id=restaurant1.id, name="Pepperoni", description="Pepperoni, mozzarella, tomato sauce", price=14.99, category="Pizza", ingredients=["pepperoni", "mozzarella", "tomato"], allergens=["dairy"], cuisine_type="Italian", is_available=True),
            MenuItem(restaurant_id=restaurant1.id, name="Spicy Diavola", description="Spicy salami, chili flakes, mozzarella", price=15.99, category="Pizza", ingredients=["salami", "chili", "mozzarella", "tomato"], allergens=["dairy"], cuisine_type="Italian", is_available=True),
            MenuItem(restaurant_id=restaurant1.id, name="Caesar Salad", description="Romaine, parmesan, croutons, caesar dressing", price=9.99, category="Salad", ingredients=["romaine", "parmesan", "croutons", "caesar dressing"], allergens=["dairy", "gluten"], cuisine_type="Italian", is_available=True),
            MenuItem(restaurant_id=restaurant1.id, name="Tiramisu", description="Coffee-soaked ladyfingers, mascarpone cream", price=7.99, category="Dessert", ingredients=["ladyfingers", "mascarpone", "coffee", "cocoa"], allergens=["dairy", "gluten"], cuisine_type="Italian", is_available=True),
        ]
        for item in pizza_items:
            db.add(item)

        sushi_items = [
            MenuItem(restaurant_id=restaurant2.id, name="Salmon Nigiri", description="Fresh Atlantic salmon over seasoned rice", price=6.99, category="Nigiri", ingredients=["salmon", "rice", "vinegar", "soy"], allergens=["fish", "soy", "gluten"], cuisine_type="Japanese", is_available=True),
            MenuItem(restaurant_id=restaurant2.id, name="Tuna Roll", description="Fresh tuna, rice, nori", price=5.99, category="Maki", ingredients=["tuna", "rice", "nori"], allergens=["fish"], cuisine_type="Japanese", is_available=True),
            MenuItem(restaurant_id=restaurant2.id, name="California Roll", description="Crab, avocado, cucumber", price=7.99, category="Maki", ingredients=["crab", "avocado", "cucumber", "rice", "nori"], allergens=["shellfish"], cuisine_type="Japanese", is_available=True),
            MenuItem(restaurant_id=restaurant2.id, name="Edamame", description="Steamed soybeans with sea salt", price=4.99, category="Appetizer", ingredients=["soybeans", "salt"], allergens=["soy"], cuisine_type="Japanese", is_available=True),
            MenuItem(restaurant_id=restaurant2.id, name="Mochi Ice Cream", description="Green tea ice cream wrapped in mochi", price=3.99, category="Dessert", ingredients=["mochi", "green tea ice cream", "sugar"], allergens=["dairy", "gluten"], cuisine_type="Japanese", is_available=True),
        ]
        for item in sushi_items:
            db.add(item)

        await db.commit()

    print("Seed data created successfully!")
    print("Admin: admin@menumind.com / admin123")
    print("Owner 1: owner@pizzeria.com / owner123 (Tony's Pizzeria)")
    print("Owner 2: owner@sushi.com / owner123 (Sakura Sushi)")
    print("Consumer 1: alice@example.com / consumer123")
    print("Consumer 2: bob@example.com / consumer123")


if __name__ == "__main__":
    asyncio.run(seed())
