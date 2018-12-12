from repositories.repository import Repository


class PriceListRepository(Repository):
    _FILENAME = "./data/PriceChart.csv"
    _TYPE = None
    _PRIMARY_KEY = "category"
    _CSV_ROW_NAMES = ["price"]

    def dict_to_model_object(self, price_list_dict):
        price_list_dict["price"] = int(price_list_dict["price"])
        return dict(price_list_dict)