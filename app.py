from flask import Flask, request, render_template
import json

with open("candidates.json", "r", encoding="utf-8") as file:
    candidates = json.load(file)

name_mapping = {candidate["name"]: candidate for candidate in candidates}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           name_mapping=name_mapping)


@app.route('/candidate/<name>/')
def candidate_page(name):
    candidate = name_mapping[name.title().replace('_', ' ')]
    return render_template("candidate.html",
                           candidate=candidate)


@app.route('/search_skill/')
def search_skill():
    skill = request.args.get('skill', default=1, type=str)

    matching_candidates = {}

    for name, info in name_mapping.items():
        if skill.lower() in info['skills'].lower().split(', '):
            matching_candidates[name] = info

    return render_template("search_skill.html",
                           matching_candidates=matching_candidates)


@app.route('/search_name/')
def search_name():
    name = request.args.get('name', default=1, type=str)

    if name.title().replace('_', ' ') not in name_mapping.keys():
        return render_template("search_name.html",
                               candidate=False)
    else:
        candidate = name_mapping[name.title().replace('_', ' ')]
        return render_template("search_name.html",
                               candidate=candidate)


if __name__ == '__main__':
    app.run()
