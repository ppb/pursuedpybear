from hypothesis import settings
settings.register_profile("x-large", max_examples=10000)
settings.register_profile("large", max_examples=1000)
settings.register_profile("jumbo", max_examples=500)
