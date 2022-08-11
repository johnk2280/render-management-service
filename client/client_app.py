import json

import click
import requests

METHOD_MAPPER = {
    'get': requests.get,
    'post': requests.post,
}


def get_response(
        method: str,
        url: str,
        data: dict = None,
        token: str = None,
) -> requests.Response:
    headers = {
        'Authorization': f'Token {token}'
    }
    response = METHOD_MAPPER[method.lower()](
        url=url,
        data=data,
        headers=headers if token else None,
    )
    return response.json()


@click.command()
@click.argument('method')
@click.argument('url')
@click.option('--u', help='Имя пользователя для регистрации')
@click.option('--p', help='Пароль для регистрации')
@click.option('--t', help='Токен для получения данных')
def main(
        method: str = None,
        url: str = None,
        u: str = None,
        p: str = None,
        t: str = None,
) -> None:
    """Клиентское CLI приложение для регистрации нового пользователя,
    получения токена зарегистрированного пользователя, получения списка задач
    пользователя и для получения истории смены статусов конкретной задачи
    зарегистрированного пользователя.

    Порядок действий:

        1. Для предоставления возможности получения данных, необходимо
        зарегистрироваться. Если вы являетесь зарегистрированным пользователем,
        то можно перейти к следующему шагу.

        Итак, что бы зарегистрироваться, необходимо направить GET запрос
        на адрес http://hostname/api/v1/registration с указанием имени
        пользователя и пароля. Примеры запроса:

        $ post http://hostname/api-token-auth/ --u=username --p=password

        Если регистрация прошла успешно, то в ответ получите json-объект
        с указанием имени пользователя:

        {

            "username": "gomerSimpson"

        }

        В противном случае сообщение с указанием ошибки.

        2. Для получения токена, необходимо отправить POST запрос на
        адрес  http://hostname/api-token-auth/ с обязательным указанием
        имени пользователя и пароля. Пример запроса:

        $ post http://hostname/api-token-auth/ --u=gomerSimpson --p=password

        В случае успешного выполнения запроса придет ответ с указанием токена:

        {

            "token": "bb79f1772ac1b86d57812d904ed89bc16cdc2991"

        }

        В противном случае сообщение с указанием ошибки.

        3. Для получения списка задач пользователя, необходимо отправить
        GET запрос на адрес http://hostname/api/v1/tasks/ с обязательным
        указанием токена. Пример запроса:

        get http://hostname/api/v1/tasks/ --t=e500ac59777571c051d405dbee9a31e7a07d2c2c

        4. Для создания новой задачи, необходимо отправить POST запрос
        на адрес http://hostname/api/v1/task_create/ с обязательным
        указанием токена. Пример запроса:

        post http://hostname/api/v1/task_create/ --t=e500ac59777571c051d405dbee9a31e7a07d2c2c

        5. Для получения истории смены статусов задачи, необходимо отправить
        GET запрос на адрес http://hostname/api/v1/task_history/<task_id:int>
        с обязательным указанием токена. Пример запроса:

        get http://hostname/api/v1/task_history/29 --t=e500ac59777571c051d405dbee9a31e7a07d2c2c


    """
    payload = {'username': u, 'password': p}
    response = get_response(
        method=method,
        url=url,
        data=payload,
        token=t,
    )
    click.echo(json.dumps(response, indent=4))


if __name__ == '__main__':
    main()
