import re
import pandas as pd


class Preprocessor:
    def _get_index_of_rows_with_no_access_to_public_transports(
            self,
            df,
            column_name
    ):
        return df[~df[column_name].str.contains('徒歩|停歩', na=False)].index

    def _get_index_of_rows_with_no_floor_numbers(
        self,
        df,
        column_name
    ):
        return df[~df[column_name].str.contains('階', na=False)].index

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
            prices = list(map(float, symbolless_price.split('～')))
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

    def _extract_room_layout(self, room_layout):
        try:
            return re.search(r'(.*) \(.*\)', room_layout).group(1)
        except AttributeError:
            return room_layout

    def _extract_build_year(self, build_date):
        return int(re.search(r'\(([0-9]*)年.*\)', build_date).group(1))

    def _extract_floor_number(self, floor):
        floor_number = int(re.search(r'([0-9]+)階', floor).group(1))

        if '地下' in floor:
            return -floor_number
        else:
            return floor_number

    def _convert_multi_categorical_variables_to_binaries(
        self,
        series,
        prefix,
        delimiter='|'
    ):
        df_output = pd.DataFrame(series)
        df_output.fillna('', inplace=True)
        splitted_series = series.str.split(delimiter, expand=True)
        unique_series = pd.unique(splitted_series.values.ravel('K'))

        for item in sorted(filter(None, unique_series)):
            column_name = '{}_{}'.format(prefix, item)
            df_output[column_name] = 0
            df_output.loc[series.str.contains(item), column_name] = 1

        # Exclude first column from the output
        return df_output.drop(df_output.columns[[0]], axis=1)

    def _convert_to_binary(self, column_value):
        if 'あり' in column_value:
            return 1
        else:
            return 0
