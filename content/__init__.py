# -*- coding: utf-8 -*-
"""Aggregates all page bodies. Each module exposes build(code, term, exercise) -> dict."""
from . import p_home, p_basics, p_concepts, p_practice, p_extra


def build_bodies(code, term, exercise):
    bodies = {}
    for mod in (p_home, p_basics, p_concepts, p_practice, p_extra):
        bodies.update(mod.build(code=code, term=term, exercise=exercise))
    return bodies
