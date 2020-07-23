import re


class Preprocessor:
    def _convert_price_str_to_float(self, price):
        if 'なし' in price:
            return 0.0
        else:
            has_ten_thousands_counter = '万' in price

            symbolless_price = re.search(r'(.*?)円', price).group(1)
            symbolless_price = (
                symbolless_price
                .replace('万', '')
                .replace(',', '')
            )

            # When property price is a price range
            # take the average of the prices as the new price
            prices = list(map(float, symbolless_price.split('〜')))
            averaged_price = sum(prices) / len(prices)

            if has_ten_thousands_counter:
                return averaged_price * 10000
            else:
                return averaged_price

    def _extract_city_of_address(self, location, prefecture, city_title):
        regex = r'(.*[{}])'.format(city_title)
        city = re.search(regex, location).group(1)

        return city.replace(prefecture, '')

    def _extract_minimum_access_time_to_public_transport(
            self,
            access_to_public_transports
    ):
        access_times = re.findall(
            r'[徒歩|停歩]([0-9]+)分',
            access_to_public_transports
        )
        access_times = list(map(int, access_times))

        return min(access_times)
