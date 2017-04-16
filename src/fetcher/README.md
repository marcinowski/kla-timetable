Timetable structure: 
```
[
    {
        'line': <#line>,
        'routes': [
            {
                'route': <route>,
                'daily': [
                    {
                        'stop': <stop_name>,
                        'hours': [ <list_of_hours > ],
                    },
                    ...
                ],
                'saturday': [ ... ],
                'sunday': [ ... ]
            },
            ...
        ],
    },
    ...
]
```