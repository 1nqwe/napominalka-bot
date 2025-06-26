import aiosqlite

async def add_user(user_id, full_name, username):
    connect = await aiosqlite.connect('bot/data_base/db.db')
    cursor = await connect.cursor()
    check_user = await cursor.execute("SELECT * FROM users WHERE (user_id) = ?", (user_id,))
    check_user = await check_user.fetchone()
    if check_user is None:
        await cursor.execute("INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)",
                             (user_id, full_name, username))
        await connect.commit()
    await cursor.close()
    await connect.close()

async def set_timezone(user_id, timezone):
    connect = await aiosqlite.connect('bot/data_base/db.db')
    cursor = await connect.cursor()
    await cursor.execute("UPDATE users SET timezone = ? WHERE user_id = ?",
                         (timezone, user_id, ))
    await connect.commit()
    await cursor.close()
    await connect.close()

async def get_timezone(user_id):
    connect = await aiosqlite.connect('bot/data_base/db.db')
    cursor = await connect.cursor()
    await cursor.execute('SELECT timezone FROM users WHERE user_id = ?', (user_id,))
    timezone = await cursor.fetchone()
    await cursor.close()
    await connect.close()
    return timezone[0]