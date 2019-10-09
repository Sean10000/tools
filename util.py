import pymysql
from yaml import load
from yaml import FullLoader


def get_yaml_config(section_name, *args):
    config_file = "config.yaml"
    with open(config_file) as f:
        config = load(f, Loader=FullLoader)
    yaml_object = config.get(section_name)
    if len(args) > 0:
        for sub_section in args:
            yaml_object = yaml_object.get(sub_section)
    return yaml_object


def get_mysql_conn(mysql_section):
    mysql_config_dict = get_yaml_config(mysql_section)
    return pymysql.connect(host=mysql_config_dict.get("host"),
                           port=mysql_config_dict.get("port"),
                           user=mysql_config_dict.get("user"),
                           password=mysql_config_dict.get("password"),
                           db=mysql_config_dict.get("db"),
                           cursorclass=pymysql.cursors.DictCursor)


def execute_mysql_select_query(mysql_conn, query):
    try:
        with mysql_conn.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            return mysql_cursor.fetchall()
    except (pymysql.err.OperationalError, pymysql.err.IntegrityError, pymysql.err.InternalError):
        return None
    except Exception as e:
        print(e)
