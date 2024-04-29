# mini-blog
Веб-приложение, позволяющее создавать текстовые блоги и
обмениваться ими.

## Основные возможности

- управление пользователями(регистрация, вход, удаление)
- Создание текстовых постов
- Просмотр своих постов
- Просмотр постов другого пользователя
- Просмотр "_ленты_"
- Оставление реакций и комментариев под постами

## Используемые библиотеки
```
fastapi==0.110.2
pydantic==2.7.1
sqlalchemy==2.0.29
pyjwt==2.8.0
bcrypt==4.1.2
```
Используемая версия `python==3.11.5`. При разработке будет использоваться
PostgresQL.

## Основные сущности

- `User`:
  - `id SERIAL PRIMARY KEY` - уникальный id каждой записи
  - `name - VARCHAR NOT NULL UNIQUE` - имя пользователя
  - `password - CHAR(60)` - захешированный пароль
- `Post`
  - `id SERIAL PRIMARY KEY` - уникальный id каждой записи
  - `header VARCHAR NOT NULL` - заголовок поста
  - `content TEXT` - контент поста
  - `likes_count INT DEFAULT 0` - количество лайков
  - `dislike-count INT DEFAULT 0` - количество дизлайков
  - `FOREIGN KEY(author_id) REFERENCES User(id) ON DELETE CASCADE` - автор поста
    - `creation_date TIMESTAMP` - дата создания
- `UserPostLike` - список пользователей, которые ставили лайки к посту
  - `id SERIAL PRIMARY KEY`
  - `FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE CASCADE`
  - `FOREIGN KEY(post_id) REFERENCES Post(id) ON DELETE CASCADE`
- `UserPostDislike` - аналогично `UserPostLike`
- `Comment`
  - `id SERIAL PRIMARY KEY`
  - `comment TEXT NOT NULL` - текст комментария
  - `FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE CASCADE` - автор комментария
  - `FOREIGN KEY(post_id) REFERENCES Post(id) ON DELETE CASCADE` - пост, к которому оставлен комментарий

Для работы с данными таблицами будут использоваться соответствующие ORM классы

## Основные пути
- `/user/registration` - создание пользователя (возвращает JWT-токен)
- `/user/login` - вход в систему (возвращает JWT-токен)
- `/user/delete` - удаление пользователя
- `/posts/` - возвращает ленту с постами(возвращает список недавних постов)
- `/posts/{id}` - возвращает пост по его `id`
- `/posts/add_like/{id}` - добавляет лайк к посту
- `/posts/add_dislike/{id}` - добавить дизлайк к посту
- `/posts/add_comment/{id}` - добавить комментарий к посту