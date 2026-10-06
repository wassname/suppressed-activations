"""Method registration and resource disclosures. — PI/OpenAI"""
TRANSFORMS = {}


def _register(kind):
    def transform(name, setting=(), fitted="nothing", about="", author="", external_data="none",
                  training="none", extras="token scores; dev-selected layer"):
        def register(fn):
            TRANSFORMS[name] = {"kind": kind, "fn": fn, "setting": tuple(setting), "fitted": fitted,
                                "about": about or name, "author": author, "function": fn.__name__,
                                "external_data": external_data, "training": training,
                                "extras": extras if kind == "unrestricted" else "none"}
            return fn
        return register
    return transform

geometry, unrestricted = _register("geometry"), _register("unrestricted")
