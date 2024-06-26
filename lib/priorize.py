#!/usr/bin/env python3
#-*-encoding:utf-8*-

import os
import sys
import random

try:
    from . import utils
    from . import pomodoro
    from . import datastore
except ImportError:
    import utils
    import pomodoro
    import datastore

def compute_cumm_probas(name, weights, k, choices=[]):
    sumw = sum(weights.values())
    probas = { k:v / sumw for k,v in weights.items() }
    if k == 1:
        return probas[name]

    result = probas.pop(name)
    for choice, prob in probas.items():
        p = compute_cumm_probas(
            name,
            { k:v for k, v in weights.items() if k != choice },
            k-1,
            choices = choices + [choice]
        )
        result += prob * p
    return result

class PrioPick:
    def __init__(self, verbose):
        self.name = []
        self.prio = []
        self.picked = []
        self.verbose = verbose

    def add(self, name, prio):
        self.name.append(name)
        self.prio.append(prio)

    def import_file(self, fname):
        if not os.path.isfile(fname):
            raise Exception(f"Cannot import file {fname}, does not exist")

        with open(fname, "r") as f:
            data = [
                line.split(":") for line in f.read().strip().split("\n")
                if not line.startswith("#") and len(line.strip()) > 0
            ]
        data = { v[0].strip(): float(v[1].strip()) for v in data }
        for name, prio in data.items():
            self.add(name, prio)

    @property
    def weights(self):
        p = {}
        for n, name in enumerate(self.name):
            if name in self.picked:
                continue
            prio = self.prio[n]
            p[name] = prio
        assert sum(p.values()) > 0
        return p
        
    @property
    def probas(self):
        p = self.weights
        psum = sum(p.values())
        return { key: val / psum for key, val in p.items() }

    def pick(self, k=1):
        choices = []
        for _ in range(0, k):
            all_probas = self.probas.items()
            keys = [p[0] for p in all_probas]
            weights = [p[1] for p in all_probas]
            if len(all_probas) == 0:
                break

            name = random.choices(keys, weights, k=1)[0]
            self.picked.append(name)
            choices.append(name)
        return choices

    def compute_probas(self, k):
        weights = self.weights
        return { n: compute_cumm_probas(n, weights, k)  for n in self.name }

    def print_probas(self, k):
        probas = self.compute_probas(k)
        nspace = max([len(n) for n in probas.keys()])
        probas = sorted(probas.items(), key=lambda x: x[1], reverse = True)
        for name, proba in probas:
            ns = nspace - len(name)
            print("{}: {}{:.3f} %".format(name, ns * " ", proba * 100))

    def print_volume_hours(self, k, hour_tot):
        probas = self.compute_probas(k)
        nspace = max([len(n) for n in probas.keys()])
        probas = sorted(probas.items(), key=lambda x: x[1], reverse = True)
        for name, proba in probas:
            nh = hour_tot * proba
            ns = nspace - len(name)
            print("{}: {}{:.2f} h".format(name, ns * " ", nh))

# per_session = 0.5
# per_week = 6
# picks.print_volume_hours(3, per_session * per_week * 4 * 12)

def act(fname, pomodoro_cache, *a, verbose = False, **args):
    if not os.path.isfile(fname):
        print("File does not exist")
        print(f"It should exist at {fname}")
        return

    pick = PrioPick(verbose)
    pick.import_file(fname)
    k = args["nb"]
    if verbose:
        print(f"Probabilities for {k} picks:")
        pick.print_probas(k)

    got = pick.pick(k)
    if any([got.count(val) != 1 for val in got]):
        raise Exception(f"Error on data: {got}")

    print("Choices:", ", ".join(got))
    if utils.yes_no_ask("Start a Pomodoro session with these tasks ?"):
        work = int(input("How many minutes per work session ? "))
        pause = int(input("How many minutes per pause ? "))
        p = pomodoro.PomodoroTimer(
           pomodoro_cache,
           tasklist=[ g.capitalize() for g in got ],
           work=work,
           pause=pause,
           **args
        )
        p.start_cli()

def setup(parser):
    parser.add_argument("name", help="Priorities set to use", type=str)
    parser.add_argument("nb", help="Number of picks to make", type=int)
    parser.add_argument("--create", "-c", help="Create a new list", action="store_true")

def autocomplete(args):
    datastore.autocomplete_datastore(["priorize"] + args)
