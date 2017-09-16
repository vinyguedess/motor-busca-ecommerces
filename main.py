import sys
from Activities import search_in_google

CLIparameters = sys.argv

activity = CLIparameters[1]
parameters = list(
    filter(
        lambda x: x is not None, 
        [item if index > 1 else None for index, item in enumerate(CLIparameters)]
    )
)

if activity == 'search':
    search_in_google(parameters)

