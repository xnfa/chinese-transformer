import argparse
import base64
import csv
import io
from pathlib import Path
from typing import List, Tuple

import aiohttp_jinja2
from aiohttp import web
import jinja2

import lm_web_ui
from lm.inference import ModelWrapper


app = web.Application()
INITIAL_TEXT = 'Она открыла дверь на'


@aiohttp_jinja2.template('index.jinja2')
def index(request):
    text = request.query.get('text', INITIAL_TEXT)
    lines_as_separate = bool(request.query.get('lines_as_separate'))
    ctx = {'text': text, 'lines_as_separate': lines_as_separate}
    model: ModelWrapper = app['model']

    if request.query.get('predict_next_token'):
        next_top_k = model.get_next_top_k(tokenize(text), top_k=10)
        next_top_k = [[token, log_prob] for log_prob, token in next_top_k]
        ctx['next_token_prediction'] = next_top_k
        ctx['next_token_prediction_csv'] = to_csv_data_url(
            next_top_k, ['token', 'log_prob'])

    elif request.query.get('score_occurred'):
        if lines_as_separate:
            texts = [t.strip() for t in text.split('\n')]
            texts = list(filter(None, texts))
        else:
            texts = [text]
        occurred_scores = []
        for i, t in enumerate(texts, 1):
            occurred_scores.extend(
                (i, token, log_prob) for log_prob, token in
                model.get_occurred_log_probs(tokenize(t)))
        ctx['occurred_scores'] = occurred_scores
        ctx['occurred_scores_csv'] = to_csv_data_url(
            occurred_scores, ['text_no', 'token', 'log_prob'])
    return ctx


def tokenize(text: str) -> List[str]:
    tokens = [app['model'].END_OF_TEXT] + app['model'].tokenize(text)
    tokens = tokens[:app['model'].model.hparams.n_ctx]
    return tokens


def to_csv_data_url(data: List[List], header: List[str]) -> str:
    """ Return data url with base64-encoded csv.
    """
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
    b64data = base64.b64encode(f.getvalue().encode('utf8')).decode('ascii')
    return f'data:text/csv;base64,{b64data}'


def main():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('model_root', type=Path)
    arg('--port', type=int, default=8000)
    arg('--host', default='localhost')
    args = parser.parse_args()

    template_root = Path(lm_web_ui.__file__).parent / 'templates'
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(template_root)))
    app['model'] = ModelWrapper.load(args.model_root)
    app.add_routes([web.get('/', index)])
    web.run_app(app, host=args.host, port=args.port)

main()
