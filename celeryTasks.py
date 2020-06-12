from celery import Celery
from scripts.dymanicLoad import get_modules


script_starter_dict = get_modules()


app = Celery('tasks')

app.config_from_object('celeryConfig')


@app.task(soft_time_limit=1800)
# 遍历所有脚本，并异步执行该包中的入口函数，入口函数必须统一命名为starter
def run_all_scripts(host, port, asset_id, is_https):

    for key in script_starter_dict.keys():
        print(key)
        try:
            if hasattr(script_starter_dict[key], "starter"):
                func = getattr(script_starter_dict[key], "starter", None)
                result = func(host, port, asset_id, is_https)
                print(result)
                return result
        except Exception as e:
            print("task outof time(already over 30 mins)")
