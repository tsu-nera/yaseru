import invoke
import src.lib.weight as weight
import src.lib.calory as calory


@invoke.task
def get_weights(c, base_date=None, end_date=None):
    weight.get_weights(base_date, end_date)


@invoke.task
def get_calories(c, base_date=None, end_date=None):
    calory.get_calories(base_date, end_date)


# def trip(c, year, month, day):
#     data_dir = "rawdata/trips"
#     # now = datetime.now()
#     # data_file = now.strftime('%y%m%d_%H%M%S') + "_trips.csv"
#     data_file = "latest_trips.csv"
#     data_path = data_dir + "/" + data_file

#     command = "cd ubereats && rm ../{} -f && scrapy crawl -a year={} -a month={} -a day={} trip -o ../{}".format(  # noqa
#         data_path, year, month, day, data_path)  # noqa
#     invoke.run(command)
