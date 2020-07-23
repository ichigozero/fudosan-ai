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
