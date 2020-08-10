import re
import pandas as pd


class Preprocessor:
    def clean_data(
            self,
            csv_path,
            prefecture_name,
            municipal_types
    ):
        df = pd.read_csv(csv_path, na_values=['-', 'ー'])

        df.fillna('', inplace=True)
        df.dropna(how='all', inplace=True)
        df.drop_duplicates(inplace=True)
        df.drop(
            self._get_index_of_rows_with_no_access_to_public_transports(
                df=df,
                column_name='access'
            ),
            inplace=True
        )
        df.drop(
            self._get_index_of_rows_with_no_floor_numbers(
                df=df,
                column_name='floor_number'
            ),
            inplace=True
        )
        df.drop(
            self._get_index_of_rows_with_no_floor_numbers(
                df=df,
                column_name='number_of_floors'
            ),
            inplace=True
        )

        df.update(df['rent_price'].apply(self._convert_price_str_to_float))
        df.update(df['monthly_fee'].apply(self._convert_price_str_to_float))

        df['total_rent_price'] = df['rent_price'] + df['monthly_fee']
        df.drop(
            self._get_index_of_rows_with_outliers(
                df=df,
                column_name='total_rent_price'
            ),
            inplace=True
        )

        df.update(
            df['location'].apply(
                self._extract_city_of_location,
                args=(prefecture_name, '|'.join(municipal_types),)
            )
        )
        df.update(
            df['access'].apply(
                self._extract_minimum_access_time_to_public_transport
            )
        )
        df.update(df['room_layout'].apply(self._extract_room_layout))
        df.update(df['build_date'].apply(self._extract_build_year))
        df.update(df['floor_number'].apply(self._extract_floor_number))
        df.update(df['number_of_floors'].apply(self._extract_floor_number))
        df.update(df['has_parking'].apply(self._convert_to_binary))

        df['room_size'] = pd.to_numeric(
            df['room_size'].str.replace('m2', '')
        )
        df = df.join(
            self._convert_multi_categorical_variables_to_binaries(
                series=df['features'],
                prefix='features'
            )
        )
        df = df.join(
            self._convert_multi_categorical_variables_to_binaries(
                series=df['popular_items'],
                prefix='popular_items'
            )
        )

        columns_to_drop = [
            'rent_price',
            'monthly_fee',
            'bond_deposit',
            'key_money',
            'security_deposit',
            'features',
            'popular_items',
            'bath_toilet',
            'kitchen',
            'storage',
            'porch',
            'security',
            'facility',
            'room_position',
            'communication',
            'rent_condition',
            'other_facility',
            'has_deduction',
            'has_insurance',
            'contract_period',
            'available_date',
            'misc_conditions',
            'special_note',
            'discloser',
            'disclose_date',
            'update_date',
            'next_update_date',
            'url',
        ]
        df.drop(columns_to_drop, axis=1, inplace=True)

        return pd.get_dummies(
            df,
            columns=[
                'location',
                'room_layout',
                'category',
                'azimuth',
                'building_structure'
            ]
        )

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

    def _get_index_of_rows_with_outliers(
        self,
        df,
        column_name
    ):
        first_quartile = df[column_name].quantile(0.25)
        third_quartile = df[column_name].quantile(0.75)

        interquartile_range = third_quartile - first_quartile
        lower_bound = first_quartile - (1.5 * interquartile_range)
        upper_bound = third_quartile + (1.5 * interquartile_range)

        return df[
            (df[column_name] < lower_bound) |
            (df[column_name] > upper_bound)
        ].index

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
            # take the average of the prices as the new price,
            # since we do not know what the actual price would be.
            prices = list(map(float, symbolless_price.split('～')))
            averaged_price = sum(prices) / len(prices)

            if has_ten_thousands_counter:
                return averaged_price * 10000
            else:
                return averaged_price

    def _extract_city_of_location(self, location, prefecture, city_title):
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
        splitted_series = series.str.split(delimiter, expand=True)
        unique_series = pd.unique(splitted_series.values.ravel('K'))

        for item in filter(None, unique_series):
            column_name = '{}_{}'.format(prefix, item)
            df_output[column_name] = 0
            df_output.loc[
                series.str.contains(str(item), na=False),
                column_name
            ] = 1

        # We only need the newly generated columns.
        return df_output.drop(df_output.columns[[0]], axis=1)

    def _convert_to_binary(self, column_value):
        if 'あり' in column_value:
            return 1
        else:
            return 0
