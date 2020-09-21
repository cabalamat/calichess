# tpcheck.py = typesentry setup

"""
Setting up typesentry for all modules.
See <https://github.com/h2oai/typesentry> 
"""

import typesentry
tc1 = typesentry.Config()

# decorator to check function arguments at runtime:
typed = tc1.typed      

# equivalent of isinstance():
is_type = tc1.is_type

#end
