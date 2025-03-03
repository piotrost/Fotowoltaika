# Piotr Ostaszewski (325697)
# script to be used in QGIS Python Console (without necessary imports etc)
# qneat3 plugin required

# paths
input_edges = 'C:/Users/piotr/Documents/pw/5/analizy/Project1/dane/aGraf/krawedzie.shp'
start_nodes = 'C:/Users/piotr/Documents/pw/5/analizy/Project1/dane/aGraf/wezly_start.shp'
output = 'C:/Users/piotr/Documents/pw/5/analizy/Project1/dane/qWezly/qWezly.tif'

processing.run(
    "qneat3:isoareaasinterpolationfromlayer",
    {
        'INPUT':input_edges,
        'START_POINTS':start_nodes,
        'ID_FIELD':'ORIG_FID',                      # unique point id field
        'MAX_DIST':'10000',                         # Size of Iso-Area (distance or time value)
        'CELL_SIZE':'5',                            # Cellsize of interpolation raster
        'STRATEGY':'0',                             # shortest path
        'ENTRY_COST_CALCULATION_METHOD':'0',        # Planar (only use with projeced CRS)
        'DIRECTION_FIELD':'',
        'VALUE_FORWARD':'',
        'VALUE_BACKWARD':'',
        'VALUE_BOTH':'',
        'DEFAULT_DIRECTION':'2',                    # Both directions
        'SPEED_FIELD':'',
        'DEFAULT_SPEED':'140',                      # km/h
        'TOLERANCE':'10',                           # Topology tolerance
        'OUTPUT':output
    }
)