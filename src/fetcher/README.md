The following query was used here http://overpass-turbo.eu/ to extract bus stops in Kalisz area.
```
[out:json];
(
    node[highway=bus_stop](51.672980972951336,17.941017150878906,51.797999847094694,18.198509216308594);
);
out+body;
>;
out+skel+qt;
 ```
 or 
 ```
[out:json];
(
    node({{bbox}})[highway=bus_stop];
    relation({{bbox}})[route=bus];
);
out+body;
>;
out+skel+qt;
 ```
 
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