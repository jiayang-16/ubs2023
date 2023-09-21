import json
import logging

from flask import request

from routes import app

from typing import Dict, List


def find_prefix(l: list, k: int, prefix: str) -> List[str]:
    res = []
    for s in l:
        if s.startswith(prefix):
            res.append(s)
            if len(res) == k:
                return res
    return res


def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
    # Fill in your solution here and return the correct output based on the given input
    clss = {}
    for dic in classes:
        for key in dic:
            members = dic[key]
            clss[key] = members
    sorted_index_dict = {'': sorted(list(clss.keys()))}
    for key in clss:
        if isinstance(clss[key], dict):
            sorted_index_dict[key] = sorted(list(clss[key].keys()))
        elif isinstance(clss[key], list):
            sorted_index_dict[key] = sorted(list(clss[key]))
        else:
            sorted_index_dict[key] = [""]
    res = {}
    for state in statements:
        search = clss
        key = ""
        state_list = state.split('.')
        for s in state_list[:-1]:
            if s in search:
                if search == clss:
                    search = search[s]
                    key = s
                else:
                    if isinstance(search, dict):
                        type_s = search[s]
                    else:
                        type_s = s
                    if type_s in clss:
                        search = clss[type_s]
                        key = type_s
                    else:
                        search = None
                        break
            else:
                search = None
                break
        if search is None:
            res[state] = [""]
        else:
            res[state] = find_prefix(sorted_index_dict[key], 5, state_list[-1])
    return res


logger = logging.getLogger(__name__)


@app.route('/lazy-developer', methods=['POST'])
def lazy_developer():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    res = getNextProbableWords(data.get("classes"), data.get("statements"))
    logging.info("My result :{}".format(res))
    return json.dumps(res)
