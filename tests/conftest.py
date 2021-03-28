from hypothesis import settings
settings.register_profile("x-large", max_examples=100*settings.default.max_examples)
settings.register_profile("large", max_examples=10*settings.default.max_examples)
settings.register_profile("jumbo", max_examples=5*settings.default.max_examples)
