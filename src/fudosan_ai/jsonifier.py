import json

from .preprocessor import Preprocessor

class Jsonifier:
    @staticmethod
    def to_json(cleaned_df):
        def _get_unique_list(column_name):
            output = cleaned_df[column_name].unique().tolist()
            output.sort()

            return output

        def _get_min_max_value(column_name):
            return [
                cleaned_df[column_name].min(),
                cleaned_df[column_name].max()
            ]

        def _get_rounded_min_max_value(column_name):
            return [
                round(cleaned_df[column_name].min(), -1),
                round(cleaned_df[column_name].max(), -1)
            ]

        def _get_multi_categorical_variables_unique_list(column_name):
            output = (
                Preprocessor
                ._get_multi_categorical_variables_unique_values(
                    series=cleaned_df[column_name])
                .tolist()
            )
            output = list(filter(None, output))
            output.sort()

            return output

        return {
            'checkbox': {
                'features': (
                    _get_multi_categorical_variables_unique_list('features')
                ),
                'popular_items': (
                    _get_multi_categorical_variables_unique_list('popular_items')
                )
            },
            'dropdown_range': {
                'access': _get_min_max_value('access'),
                'build_date': _get_min_max_value('build_date'),
                'room_size': _get_rounded_min_max_value('room_size'),
                'floor_number': _get_min_max_value('floor_number'),
                'number_of_floors': _get_min_max_value('number_of_floors')
            },
            'dropdown_choice': {
                'location': _get_unique_list('location'),
                'room_layout': _get_unique_list('room_layout'),
                'category': _get_unique_list('category'),
                'azimuth': _get_unique_list('azimuth'),
                'building_structure': _get_unique_list('building_structure')
            },
            'radiobutton': {
                'has_parking': _get_unique_list('has_parking')
            }
        }
