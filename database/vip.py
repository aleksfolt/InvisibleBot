import time
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import AsyncSessionLocal, Subscription


async def add_or_update_subscription(user_id: int, duration: int):
    async with AsyncSessionLocal() as session:
        current_time = int(time.time())
        extension_time = duration * 86400

        try:
            result = await session.execute(select(Subscription).filter_by(user_id=user_id))
            subscription = result.scalars().first()

            if subscription:
                if subscription.subscription_end > current_time:
                    subscription.subscription_end += extension_time
                else:
                    subscription.subscription_end = current_time + extension_time
            else:
                new_subscription = Subscription(
                    user_id=user_id,
                    subscription_end=current_time + extension_time
                )
                session.add(new_subscription)

            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Ошибка при работе с базой данных: {e}")
        finally:
            await session.close()


async def get_subscription_end(user_id: int) -> str:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Subscription).filter_by(user_id=user_id))
            subscription = result.scalars().first()

            if subscription:
                subscription_end = datetime.utcfromtimestamp(subscription.subscription_end).strftime('%d.%m.%Y')
                return f"активна до: {subscription_end}"
            else:
                return "нет активной подписки"
        except SQLAlchemyError as e:
            print(f"Ошибка при получении подписки: {e}")
            return "ошибка при получении данных"
        finally:
            await session.close()


async def check_subscription(user_id: int):
    async with AsyncSessionLocal() as session:
        current_time = int(time.time())

        try:
            result = await session.execute(select(Subscription).filter_by(user_id=user_id))
            subscription = result.scalars().first()

            if subscription:
                if subscription.subscription_end > current_time:
                    print("Подписка активна")
                    return True
                else:
                    await session.delete(subscription)
                    await session.commit()
                    print("Подписка истекла")
                    return False
            else:
                print("Подписки нет")
                return False

        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Ошибка при работе с базой данных: {e}")
        finally:
            await session.close()


