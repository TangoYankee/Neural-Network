import os
import csv
import settings
import sql_manager


# data_dir = settings.DATA_DIR
# cancer_data_name = "cancer_data.csv"
# ep_data_name = "ep_data.csv"
# pnn_data_name = "pnn_data.csv"

# cancer_data_open = open(os.path.join(data_dir, cancer_data_name))
# ep_data_open = open(os.path.join(data_dir, ep_data_name))
# pnn_data_open = open(os.path.join(data_dir, pnn_data_name))

# cancer_data_reader = csv.reader(cancer_data_open)
# pipeline = hello_world.BasePipeline()
# for cancer_data_row in cancer_data_reader:
#     item = {
#         'values': list(map(float, cancer_data_row))
#     }
#     pipeline.process_cancer(item)
# pipeline.query_database()

# #Return a reader
# def get_from_csv(file_name):
#     data_open = open(os.path.join(settings.DATA_DIR, file_name))
#     return csv.reader(data_open)

