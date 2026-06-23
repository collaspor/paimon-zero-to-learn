# -*- coding: utf-8 -*-
"""Aggregates all page bodies. Each module exposes build(code, term, exercise) -> dict."""
from . import p_home, p_basics, p_concepts, p_practice, p_extra
from . import p_ecosystem, p_platform


def build_bodies(code, term, exercise):
    bodies = {}
    for mod in (p_home, p_basics, p_concepts, p_practice, p_extra,
                p_ecosystem, p_platform):
        bodies.update(mod.build(code=code, term=term, exercise=exercise))
    return bodies
