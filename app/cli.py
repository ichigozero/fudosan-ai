import datetime
import hashlib
import pathlib
import os
import sys

import click
from flask import Blueprint

from app import mongo
from app.data.jsonifier import Jsonifier
from app.data.model import Model
from app.data.preprocessor import Preprocessor

bp = Blueprint('cli', __name__, static_folder='static')


@bp.cli.command()
@click.argument('csv_path')
@click.argument('prefecture_name')
@click.option('municipal_types', '-m', multiple=True, default=['区', '市', '郡'])
@click.option('--set-as-active', '-s', is_flag=True)
def analyze_rent_data(
        csv_path,
        prefecture_name,
        municipal_types,
        set_as_active
):
    csv_md5 = md5(csv_path)
    documents = mongo.db.models.find({'csv_checksum': csv_md5})

    if documents.count() > 0:
        click.echo('{} has been analyzed before'.format(csv_path))
        click.echo('Aborting...')
        sys.exit()

    save_dir_path = os.path.join(bp.static_folder, prefecture_name)
    pathlib.Path(save_dir_path).mkdir(parents=True, exist_ok=True)

    pickle_name = '{}_{}.pkl'.format(
        prefecture_name,
        datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    )
    pickle_path = os.path.join(save_dir_path, pickle_name)

    preprocessor = Preprocessor()
    model = Model()

    click.echo('Cleaning CSV data')
    cleaned_df = preprocessor.clean_data(
        csv_path,
        prefecture_name,
        municipal_types
    )
    one_hot_encoded_df = preprocessor.one_hot_encode(cleaned_df)

    click.echo('Training model of cleaned CSV data')
    model.train(one_hot_encoded_df)

    click.echo('Saving trained model to {}'.format(pickle_path))
    model.to_pickle(pickle_path)

    form_elements = Jsonifier.to_json(cleaned_df)
    training_mean_abs_error = model.get_training_set_mean_absolute_error()
    test_mean_abs_error = model.get_test_set_mean_absolute_error()
    pickle_md5 = md5(pickle_path)

    is_set_to_active = set_as_active

    if set_as_active:
        # Only one trained model given
        # prefecture name can be used at one time
        mongo.db.models.update_many(
            filter={'prefecture': prefecture_name},
            update={'$set': {'active': False}}
        )
    else:
        # Make sure that there will always be
        # one active trained model given prefecture name
        active_documents = mongo.db.models.find({
            'prefecture': prefecture_name,
            'active': True
        })

        if active_documents.count() == 0:
            is_set_to_active = True

    document = {
        'csv_checksum': csv_md5,
        'prefecture': prefecture_name,
        'form_elements': form_elements,
        'model': {
            'pickle_path': pickle_path,
            'checksum': pickle_md5,
            'mean_abs_error': {
                'training': training_mean_abs_error,
                'test': test_mean_abs_error
            }
        },
        'active': is_set_to_active
    }

    click.echo('Saving analyzed data to DB')
    mongo.db.models.insert(document)


def md5(filename):
    click.echo('Calculating cheksum of {}'.format(filename))

    hash_md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)

        return hash_md5.hexdigest()
