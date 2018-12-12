class Utils(object):
    def process_yes_no_answer(self, yes_no):
            if yes_no:
                yes_no = str(yes_no)[0].upper()
                if yes_no in ["J", "Y"]:
                    return True
                return False

    def count_days_in_range(self, datetime_1, datetime_2):
        return abs((datetime_1 - datetime_2).days)

    def calculate_base_cost(self, car, pickup_datetime, return_datetime):
        days = self.count_days_in_range(pickup_datetime, return_datetime)
        day_cost = car.category["price"]
        return days * day_cost
