ENV = 'test'


class App:
    __db_config = {
        'prod': dict(
            provider='postgres',
            user='',
            password='',
            host='',
            database=''
        ),
        'dev': dict(
            provider='postgres',
            user='postgres',
            password='postgres',
            host='127.0.0.1',
            database='awstest'
        ),
        'test': dict(
            provider='postgres',
            user='postgres',
            password='postgres',
            host='127.0.0.1',
            database='awstest'
        ),
    }

    @staticmethod
    def get_db_configuration(env='test'):
        return App.__db_config[env]
